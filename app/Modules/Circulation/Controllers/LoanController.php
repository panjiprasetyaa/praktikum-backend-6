<?php

namespace Modules\Circulation\Controllers;

use App\Http\Controllers\Controller;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\DB;
use Modules\Catalog\Models\Book;
use Modules\Circulation\Models\Loan;
use Modules\Circulation\Services\CirculationService;
use Modules\Membership\Models\Member;
use Modules\Shared\Exceptions\InsufficientStockException;
use Modules\Shared\Exceptions\MemberNotEligibleException;

class LoanController extends Controller
{
    /**
     * Menampilkan daftar peminjaman (dengan Eager Loading) & form transaksi peminjaman.
     */
    public function index()
    {
        DB::flushQueryLog();
        DB::enableQueryLog();

        $loans = Loan::with(['member', 'details', 'fines'])
            ->latest('borrowed_at')
            ->paginate(10);

        $queryCount = count(DB::getQueryLog());

        $members = Member::orderBy('name')->get();
        $books = Book::orderBy('title')->get();

        return view('library.loans.index', compact('loans', 'members', 'books', 'queryCount'));
    }

    /**
     * Memproses transaksi peminjaman atomik (Database Transaction + Auto-Rollback).
     */
    public function store(Request $request, CirculationService $circulationService)
    {
        $validated = $request->validate([
            'member_id' => ['required', 'integer', 'exists:members,id'],
            'book_ids' => ['required', 'array', 'min:1'],
            'book_ids.*' => ['integer', 'exists:books,id'],
            'loan_days' => ['nullable', 'integer', 'min:1', 'max:30'],
        ]);

        try {
            $loan = $circulationService->borrowBooks(
                memberId: (int) $validated['member_id'],
                bookIds: array_map('intval', $validated['book_ids']),
                loanDays: (int) ($validated['loan_days'] ?? 7)
            );

            return redirect()->route('library.loans.index')
                ->with('success', "Transaksi Peminjaman {$loan->loan_code} BERHASIL (Atomik Commit + Domain Event BookBorrowed dipicu).");
        } catch (InsufficientStockException | MemberNotEligibleException $e) {
            return redirect()->route('library.loans.index')
                ->withInput()
                ->with('error', "ROLLBACK TRANSAKSI: {$e->getMessage()} (Tidak ada data yang disimpan).");
        } catch (\Throwable $e) {
            return redirect()->route('library.loans.index')
                ->withInput()
                ->with('error', "Gagal memproses peminjaman: {$e->getMessage()}");
        }
    }

    /**
     * Memproses pengembalian buku dan penghitungan denda otomatis.
     */
    public function returnLoan(int $id, CirculationService $circulationService)
    {
        $loan = $circulationService->returnLoan($id);
        $fine = $loan->fines->first();

        $msg = "Buku pada peminjaman {$loan->loan_code} berhasil dikembalikan dan stok katalog telah dipulihkan.";
        if ($fine && $fine->total_fine > 0) {
            $msg .= " Denda keterlambatan tercatat: Rp " . number_format($fine->total_fine, 0, ',', '.') . ".";
        }

        return redirect()->route('library.loans.index')->with('success', $msg);
    }

    /**
     * Soft delete riwayat peminjaman.
     */
    public function destroy(Loan $loan)
    {
        $code = $loan->loan_code;
        $loan->delete();

        return redirect()->route('library.loans.index')
            ->with('success', "Data peminjaman {$code} dipindahkan ke Trash (Soft Delete).");
    }

    /**
     * Menampilkan daftar peminjaman terhapus khusus Admin.
     */
    public function trash()
    {
        $trashedLoans = Loan::onlyTrashed()->with(['member', 'details'])->latest('deleted_at')->paginate(10);
        return view('library.loans.trash', compact('trashedLoans'));
    }

    /**
     * Mengembalikan data peminjaman terhapus (Restore oleh Admin).
     */
    public function restore(int $id)
    {
        $loan = Loan::onlyTrashed()->findOrFail($id);
        $loan->restore();

        return redirect()->route('library.loans.trash')
            ->with('success', "Data peminjaman {$loan->loan_code} berhasil di-restore oleh Admin.");
    }
}
