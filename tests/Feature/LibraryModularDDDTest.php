<?php

namespace Tests\Feature;

use Illuminate\Foundation\Testing\RefreshDatabase;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Event;
use Illuminate\Support\Facades\Log;
use Modules\Catalog\Models\Book;
use Modules\Catalog\Models\Category;
use Modules\Circulation\Events\BookBorrowed;
use Modules\Circulation\Models\Loan;
use Modules\Circulation\Models\LoanDetail;
use Modules\Circulation\Services\CirculationService;
use Modules\Membership\Models\Member;
use Modules\Membership\Models\Role;
use Modules\Shared\Exceptions\InsufficientStockException;
use Modules\Shared\Exceptions\MemberNotEligibleException;
use Modules\Shared\ValueObjects\Denda;
use Modules\Shared\ValueObjects\ISBN;
use Tests\TestCase;

class LibraryModularDDDTest extends TestCase
{
    use RefreshDatabase;

    protected function setUp(): void
    {
        parent::setUp();
        // Seed database
        $this->seed(\Database\Seeders\LibrarySeeder::class);
    }

    /**
     * TEST 1: Relasi Lanjutan (20% Bobot)
     * - Many-to-Many pivot dengan added_at: Buku <-> Kategori
     * - Self-referencing: Kategori Induk <-> Sub-kategori
     * - HasMany: Peminjaman <-> DetailPeminjaman
     */
    public function test_relasi_lanjutan(): void
    {
        // a. Self-referencing Category
        $parent = Category::whereNull('parent_id')->first();
        $this->assertNotNull($parent);
        $this->assertGreaterThan(0, $parent->children()->count());

        $child = $parent->children()->first();
        $this->assertEquals($parent->id, $child->parent->id);

        // b. Many-to-Many dengan Pivot added_at
        $book = Book::with('categories')->first();
        $this->assertNotNull($book);
        $this->assertGreaterThan(0, $book->categories->count());

        $category = $book->categories->first();
        $this->assertNotNull($category->pivot->added_at);

        // c. HasMany Peminjaman -> DetailPeminjaman
        $member = Member::where('status', 'active')->first();
        $service = app(CirculationService::class);
        $loan = $service->borrowBooks($member->id, [$book->id]);

        $this->assertInstanceOf(Loan::class, $loan);
        $this->assertGreaterThan(0, $loan->details()->count());
        $this->assertEquals($book->title, $loan->details->first()->book_title);
    }

    /**
     * TEST 2: Query Optimization & Eager Loading (15% Bobot)
     * - Menghindari N+1 query dengan with()
     * - Query Scopes: available(), search(), byCategory()
     */
    public function test_query_optimization_dan_scopes(): void
    {
        // a. Query Scopes
        $availableBooks = Book::available()->get();
        foreach ($availableBooks as $b) {
            $this->assertTrue($b->is_active);
            $this->assertGreaterThan(0, $b->stock);
        }

        $searchBooks = Book::search('Clean Code')->get();
        $this->assertNotEmpty($searchBooks);

        $techCategory = Category::where('slug', 'teknologi')->first();
        $catBooks = Book::byCategory($techCategory->id)->get();
        $this->assertNotEmpty($catBooks);

        // b. Eager Loading vs N+1 Query Proof
        DB::flushQueryLog();
        DB::enableQueryLog();

        // Menggunakan Eager Loading
        $loans = Loan::with(['details', 'member'])->get();
        foreach ($loans as $l) {
            $detailCount = $l->details->count();
            $memberName = $l->member?->name;
        }

        $queryCountWithEager = count(DB::getQueryLog());
        // Hanya perlu sedikit query teroptimasi
        $this->assertLessThanOrEqual(4, $queryCountWithEager);
    }

    /**
     * TEST 3: Database Transaction & Konsistensi Aggregate (20% Bobot)
     * - Operasi atomik: kurangi stok, buat loan & details
     * - Auto-rollback jika stok tidak cukup (InsufficientStockException)
     */
    public function test_database_transaction_dan_rollback(): void
    {
        $service = app(CirculationService::class);
        $member = Member::where('status', 'active')->first();

        // 1. Sukses Transaksi
        $cleanCode = Book::where('slug', 'clean-code')->first();
        $initialStock = $cleanCode->stock;

        $loan = $service->borrowBooks($member->id, [$cleanCode->id]);
        $cleanCode->refresh();

        $this->assertEquals($initialStock - 1, $cleanCode->stock);
        $this->assertDatabaseHas('loans', ['id' => $loan->id]);
        $this->assertDatabaseHas('loan_details', ['loan_id' => $loan->id, 'book_id' => $cleanCode->id]);

        // 2. Transaksi GAGAL & ROLLBACK (Buku stok 0)
        $zeroStockBook = Book::where('slug', 'pragmatic-programmer')->first();
        $this->assertEquals(0, $zeroStockBook->stock);

        $initialLoanCount = Loan::count();
        $initialDetailCount = LoanDetail::count();

        $threwException = false;
        try {
            // Coba pinjam 2 buku sekaligus: buku stok ada + buku stok kosong
            $service->borrowBooks($member->id, [$cleanCode->id, $zeroStockBook->id]);
        } catch (InsufficientStockException $e) {
            $threwException = true;
        }

        $this->assertTrue($threwException, 'InsufficientStockException harus dilempar.');
        // Pastikan tidak ada data yang tersimpan karena ROLLBACK
        $this->assertEquals($initialLoanCount, Loan::count(), 'Jumlah Loan tidak boleh bertambah setelah rollback.');
        $this->assertEquals($initialDetailCount, LoanDetail::count(), 'Detail tidak boleh tersimpan setelah rollback.');
    }

    /**
     * TEST 4: Soft Deletes & Restore (10% Bobot)
     * - Terapkan pada Buku, Anggota, dan Peminjaman
     */
    public function test_soft_deletes_dan_restore(): void
    {
        $book = Book::first();
        $id = $book->id;

        $book->delete();
        $this->assertSoftDeleted('books', ['id' => $id]);
        $this->assertNull(Book::find($id));
        $this->assertNotNull(Book::withTrashed()->find($id));

        // Restore
        $book->restore();
        $this->assertNotNull(Book::find($id));
    }

    /**
     * TEST 5: Domain Event BookBorrowed (15% Bobot)
     */
    public function test_domain_event_dispatched(): void
    {
        Event::fake([BookBorrowed::class]);

        $service = app(CirculationService::class);
        $member = Member::where('status', 'active')->first();
        $book = Book::available()->first();

        $service->borrowBooks($member->id, [$book->id]);

        Event::assertDispatched(BookBorrowed::class, function ($event) use ($book) {
            return $event->loan->details->pluck('book_id')->contains($book->id);
        });
    }

    /**
     * TEST 6: Value Objects (ISBN & Denda) (15% Bobot)
     */
    public function test_value_objects_isbn_dan_denda(): void
    {
        // Valid ISBN-13
        $isbn13 = new ISBN('978-0-13-235088-4');
        $this->assertEquals('978-0-13-235088-4', $isbn13->getValue());

        // Test Denda Value Object
        $denda = Denda::fromDays(5, 2000.0);
        $this->assertEquals(5, $denda->getDaysOverdue());
        $this->assertEquals(10000.0, $denda->getAmount());
        $this->assertEquals('Rp 10.000', $denda->formatRupiah());

        // Invalid ISBN throws InvalidArgumentException
        $this->expectException(\InvalidArgumentException::class);
        new ISBN('123-INVALID-456');
    }
}
