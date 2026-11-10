<?php

namespace Tests\Feature;

use App\Models\User;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Modules\Catalog\Models\Book;
use Modules\Catalog\Models\Category;
use Modules\Circulation\Models\Loan;
use Modules\Membership\Models\Member;
use Tests\TestCase;

class LibraryWebTest extends TestCase
{
    use RefreshDatabase;

    protected User $admin;

    protected function setUp(): void
    {
        parent::setUp();
        $this->seed(\Database\Seeders\DatabaseSeeder::class);
        $this->admin = User::where('role', 'admin')->first();
    }

    public function test_web_catalog_index_filter_and_admin_restore(): void
    {
        // 1. Index + Eager loading + Scopes
        $res = $this->actingAs($this->admin)->get(route('library.books.index', ['search' => 'Clean Code', 'available' => 1]));
        $res->assertStatus(200);
        $res->assertSee('Clean Code');

        // 2. Soft delete & Admin Restore
        $book = Book::first();
        $this->actingAs($this->admin)->delete(route('library.books.destroy', $book->id))->assertRedirect();
        $this->assertSoftDeleted('books', ['id' => $book->id]);

        $this->actingAs($this->admin)->get(route('library.books.trash'))->assertStatus(200)->assertSee($book->title);
        $this->actingAs($this->admin)->post(route('library.books.restore', $book->id))->assertRedirect();
        $this->assertNotSoftDeleted('books', ['id' => $book->id]);
    }

    public function test_web_members_index_and_admin_restore(): void
    {
        $this->actingAs($this->admin)->get(route('library.members.index'))->assertStatus(200)->assertSee('Panji Prasetya');

        $member = Member::first();
        $this->actingAs($this->admin)->delete(route('library.members.destroy', $member->id))->assertRedirect();
        $this->assertSoftDeleted('members', ['id' => $member->id]);

        $this->actingAs($this->admin)->get(route('library.members.trash'))->assertStatus(200)->assertSee($member->name);
        $this->actingAs($this->admin)->post(route('library.members.restore', $member->id))->assertRedirect();
        $this->assertNotSoftDeleted('members', ['id' => $member->id]);
    }

    public function test_web_loans_transaction_success_and_rollback(): void
    {
        $member = Member::where('status', 'active')->first();
        $goodBook = Book::where('stock', '>', 0)->first();
        $zeroBook = Book::where('stock', 0)->first();

        // 1. Sukses peminjaman lewat Web Form
        $res = $this->actingAs($this->admin)->post(route('library.loans.store'), [
            'member_id' => $member->id,
            'book_ids' => [$goodBook->id],
            'loan_days' => 7,
        ]);
        $res->assertRedirect(route('library.loans.index'));
        $res->assertSessionHas('success');

        // 2. Gagal & Rollback lewat Web Form (buku stok 0)
        $countBefore = Loan::count();
        $resFail = $this->actingAs($this->admin)->post(route('library.loans.store'), [
            'member_id' => $member->id,
            'book_ids' => [$zeroBook->id],
            'loan_days' => 7,
        ]);
        $resFail->assertRedirect(route('library.loans.index'));
        $resFail->assertSessionHas('error');
        $this->assertEquals($countBefore, Loan::count());

        // 3. Halaman Index tampil mulus
        $this->actingAs($this->admin)->get(route('library.loans.index'))->assertStatus(200);
    }
}
