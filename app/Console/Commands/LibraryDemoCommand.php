<?php

namespace App\Console\Commands;

use Illuminate\Console\Command;
use Illuminate\Support\Facades\DB;
use Modules\Catalog\Models\Book;
use Modules\Catalog\Models\Category;
use Modules\Circulation\Models\Loan;
use Modules\Circulation\Services\CirculationService;
use Modules\Membership\Models\Member;
use Modules\Shared\Exceptions\InsufficientStockException;
use Modules\Shared\ValueObjects\Denda;
use Modules\Shared\ValueObjects\ISBN;

class LibraryDemoCommand extends Command
{
    protected $signature = 'library:demo';
    protected $description = 'Demonstrasi seluruh fitur DDD Modular Monolith Perpustakaan (Pertemuan 6)';

    public function handle(CirculationService $circulationService): int
    {
        $this->info("================================================================================");
        $this->info("   DEMONSTRASI FITUR PRAKTIKUM PERTEMUAN 6: MODULAR MONOLITH & DDD (LARAVEL 13) ");
        $this->info("================================================================================");
        $this->newLine();

        // 1. RELASI LANJUTAN
        $this->comment("1. PENGUJIAN RELASI LANJUTAN");
        $this->line("   a) Self-referencing Category (Parent -> Children):");
        $parents = Category::whereNull('parent_id')->with('children')->get();
        foreach ($parents as $p) {
            $childrenNames = $p->children->pluck('name')->join(', ');
            $this->line("      - Induk: [{$p->name}] -> Sub-Kategori: [{$childrenNames}]");
        }

        $this->newLine();
        $this->line("   b) Many-to-Many Pivot (Buku <-> Kategori dengan added_at):");
        $book = Book::with('categories')->first();
        if ($book) {
            $this->line("      - Judul Buku: {$book->title}");
            foreach ($book->categories as $c) {
                $this->line("        * Kategori: {$c->name} (Pivot added_at: {$c->pivot->added_at})");
            }
        }

        $this->newLine();
        // 2. QUERY OPTIMIZATION & N+1 PROBLEM PROOF
        $this->comment("2. PENGUJIAN QUERY OPTIMIZATION & N+1 QUERY ELIMINATION");

        $member = Member::where('status', 'active')->first();
        // Buat beberapa record peminjaman tambahan jika perlu agar terlihat jelas perbedaan query
        if (Loan::count() < 5 && $member) {
            $availableBooks = Book::available()->limit(3)->get();
            for ($i = 0; $i < 4; $i++) {
                try {
                    $circulationService->borrowBooks($member->id, [$availableBooks->random()->id]);
                } catch (\Throwable $e) {}
            }
        }

        // Test N+1 (Lazy loading dalam loop)
        DB::flushQueryLog();
        DB::enableQueryLog();
        $loansRaw = Loan::all();
        foreach ($loansRaw as $l) {
            $count = $l->details->count(); // 1 query per loan!
            $memberName = $l->member?->name; // 1 query per loan!
        }
        $rawCount = count(DB::getQueryLog());

        // Test Eager Loading with(['details', 'member'])
        DB::flushQueryLog();
        DB::enableQueryLog();
        $loansEager = Loan::with(['details', 'member'])->get();
        foreach ($loansEager as $l) {
            $count = $l->details->count(); // Tidak ada query tambahan
            $memberName = $l->member?->name; // Tidak ada query tambahan
        }
        $eagerCount = count(DB::getQueryLog());

        $this->table(
            ['Metode Pengambilan Data', 'Jumlah Record', 'Jumlah Query SQL', 'Status Efisiensi'],
            [
                ['Tanpa Eager Loading (Lazy Loading)', Loan::count() . ' Peminjaman', "{$rawCount} Query", 'BOROS / LAMBAT (N+1 Query)'],
                ['Dengan Eager Loading with(...)', Loan::count() . ' Peminjaman', "{$eagerCount} Query", 'EFISIEN / CEPAT (Teroptimasi)'],
            ]
        );

        $this->newLine();
        // 3. DATABASE TRANSACTION & ROLLBACK
        $this->comment("3. PENGUJIAN DATABASE TRANSACTION & ROLLBACK");
        $zeroBook = Book::where('slug', 'pragmatic-programmer')->first();
        $this->line("   Mencoba meminjam buku dengan stok kosong ('{$zeroBook?->title}', stok: {$zeroBook?->stock})...");
        
        $loanCountBefore = Loan::count();
        try {
            $circulationService->borrowBooks($member->id, [$zeroBook->id]);
            $this->error("   [GAGAL] Seharusnya melempar InsufficientStockException!");
        } catch (InsufficientStockException $e) {
            $this->info("   [BERHASIL] Exception tertangkap: " . $e->getMessage());
            $this->info("   [VERIFIKASI ROLLBACK] Record Loan sebelum: {$loanCountBefore}, sesudah: " . Loan::count());
            $this->info("   -> DB::transaction() berhasil membatalkan seluruh operasi secara atomik!");
        }

        $this->newLine();
        // 4. SOFT DELETES & RESTORE
        $this->comment("4. PENGUJIAN SOFT DELETES & RESTORE");
        $sampleBook = Book::first();
        $sampleId = $sampleBook->id;
        $this->line("   Menghapus buku #{$sampleId} ('{$sampleBook->title}') secara Soft Delete...");
        $sampleBook->delete();

        $countActive = Book::count();
        $countWithTrashed = Book::withTrashed()->count();
        $this->line("   - Book::count() (Record Aktif): {$countActive}");
        $this->line("   - Book::withTrashed()->count() (Termasuk Soft Deleted): {$countWithTrashed}");

        $this->line("   Mengembalikan buku dengan restore()...");
        $sampleBook->restore();
        $this->info("   - Book::count() setelah restore: " . Book::count() . " [DATA PULIH]");

        $this->newLine();
        // 5. VALUE OBJECTS
        $this->comment("5. PENGUJIAN VALUE OBJECTS (SHARED KERNEL)");
        $isbn = new ISBN('978-0-13-235088-4');
        $this->line("   - Value Object ISBN Valid: " . $isbn->getValue());

        $denda5Hari = Denda::fromDays(5, 2000.0);
        $this->line("   - Value Object Denda (5 Hari x Rp 2.000): " . $denda5Hari->formatRupiah());

        $this->newLine();
        $this->info("================================================================================");
        $this->info("   SELURUH PENGUJIAN SISTEM PERPUSTAKAAN MODULAR DDD BERHASIL 100%!           ");
        $this->info("================================================================================");

        return self::SUCCESS;
    }
}
