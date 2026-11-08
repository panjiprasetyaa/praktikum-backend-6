<?php

namespace Modules\Circulation\Services;

use Illuminate\Support\Facades\DB;
use Modules\Circulation\Events\BookBorrowed;
use Modules\Circulation\Models\Fine;
use Modules\Circulation\Models\Loan;
use Modules\Circulation\Models\LoanDetail;
use Modules\Shared\Contracts\BookServiceInterface;
use Modules\Shared\Contracts\MemberServiceInterface;
use Modules\Shared\Exceptions\InsufficientStockException;
use Modules\Shared\Exceptions\MemberNotEligibleException;
use Modules\Shared\ValueObjects\Denda;

class CirculationService
{
    public function __construct(
        private readonly BookServiceInterface $bookService,
        private readonly MemberServiceInterface $memberService
    ) {}

    /**
     * Memproses peminjaman buku dalam satu Database Transaction atomik.
     *
     * @param int $memberId
     * @param array<int> $bookIds
     * @param int $loanDays
     * @return Loan
     * @throws MemberNotEligibleException|InsufficientStockException
     */
    public function borrowBooks(int $memberId, array $bookIds, int $loanDays = 7): Loan
    {
        return DB::transaction(function () use ($memberId, $bookIds, $loanDays) {
            // 1. Validasi Keaktifan Anggota melalui Contract
            if (!$this->memberService->canBorrow($memberId)) {
                throw new MemberNotEligibleException("Member #{$memberId} berstatus tidak aktif atau telah melebihi batas pinjam.");
            }

            // 2. Buat Record Induk Peminjaman (Aggregate Root)
            $loan = Loan::create([
                'loan_code'   => 'LOAN-' . date('Ymd') . '-' . strtoupper(substr(uniqid(), -5)),
                'member_id'   => $memberId,
                'borrowed_at' => now(),
                'due_date'    => now()->addDays($loanDays),
                'status'      => 'borrowed',
            ]);

            // 3. Iterasi setiap buku, validasi stok, catat snapshot, dan kurangi stok
            foreach ($bookIds as $bookId) {
                // Ambil snapshot data buku
                $bookData = $this->bookService->getBookForLoan($bookId);
                if (!$bookData) {
                    throw new \Exception("Buku dengan ID #{$bookId} tidak ditemukan dalam katalog.");
                }

                // Cek ketersediaan stok
                if (!$this->bookService->isStockAvailable($bookId, 1)) {
                    // Memicu InsufficientStockException -> Transaksi otomatis di-rollback!
                    throw new InsufficientStockException(
                        bookTitle: $bookData['title'],
                        availableStock: $bookData['stock'],
                        requestedQuantity: 1
                    );
                }

                // Simpan Snapshot ke Detail Peminjaman (DDD Invariant: Histori tidak terpengaruh perubahan master)
                LoanDetail::create([
                    'loan_id'    => $loan->id,
                    'book_id'    => $bookId,
                    'book_title' => $bookData['title'],
                    'book_isbn'  => $bookData['isbn'],
                ]);

                // Kurangi stok buku secara atomik melalui contract
                $this->bookService->reduceStock($bookId, 1);
            }

            // 4. Dispatch Domain Event
            event(new BookBorrowed($loan->load('details')));

            return $loan->load('details');
        });
    }

    /**
     * Memproses pengembalian buku, kalkulasi denda otomatis, dan restorasi stok.
     */
    public function returnLoan(int $loanId): Loan
    {
        return DB::transaction(function () use ($loanId) {
            $loan = Loan::with('details')->findOrFail($loanId);

            if ($loan->status === 'returned') {
                return $loan;
            }

            $now = now();
            $loan->returned_at = $now;
            $loan->status = 'returned';
            $loan->save();

            // Kembalikan stok setiap buku
            foreach ($loan->details as $detail) {
                $detail->returned_at = $now;
                $detail->save();

                $this->bookService->restoreStock($detail->book_id, 1);
            }

            // Hitung denda jika terlambat (menggunakan Value Object Denda)
            if ($now->greaterThan($loan->due_date)) {
                $daysOverdue = (int) ceil($loan->due_date->diffInDays($now));
                $dendaVo = Denda::fromDays($daysOverdue, 2000.0);

                Fine::create([
                    'loan_id'      => $loan->id,
                    'days_overdue' => $dendaVo->getDaysOverdue(),
                    'daily_rate'   => $dendaVo->getDailyRate(),
                    'total_fine'   => $dendaVo->getAmount(),
                    'is_paid'      => false,
                ]);
            }

            return $loan->fresh(['details', 'fines']);
        });
    }
}
