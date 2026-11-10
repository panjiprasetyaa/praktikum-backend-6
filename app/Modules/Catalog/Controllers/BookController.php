<?php

namespace Modules\Catalog\Controllers;

use App\Http\Controllers\Controller;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Str;
use Modules\Catalog\Models\Book;
use Modules\Catalog\Models\Category;
use Modules\Shared\ValueObjects\ISBN;

class BookController extends Controller
{
    /**
     * Menampilkan daftar buku dengan Eager Loading dan Query Scopes.
     */
    public function index(Request $request)
    {
        DB::flushQueryLog();
        DB::enableQueryLog();

        $books = Book::with('categories')
            ->when($request->filled('search'), fn($q) => $q->search($request->string('search')))
            ->when($request->filled('category_id'), fn($q) => $q->byCategory((int) $request->input('category_id')))
            ->when($request->boolean('available'), fn($q) => $q->available())
            ->latest()
            ->paginate(10)
            ->withQueryString();

        $categories = Category::with('children')->whereNull('parent_id')->get();
        $queryCount = count(DB::getQueryLog());

        return view('library.books.index', compact('books', 'categories', 'queryCount'));
    }

    /**
     * Menampilkan form tambah buku baru.
     */
    public function create()
    {
        $categories = Category::all();
        return view('library.books.create', compact('categories'));
    }

    /**
     * Menyimpan buku baru dengan validasi Value Object ISBN.
     */
    public function store(Request $request)
    {
        $validated = $request->validate([
            'isbn' => ['required', 'string', 'unique:books,isbn'],
            'title' => ['required', 'string', 'max:255'],
            'author' => ['required', 'string', 'max:255'],
            'publisher' => ['nullable', 'string', 'max:255'],
            'description' => ['nullable', 'string'],
            'stock' => ['required', 'integer', 'min:0'],
            'category_ids' => ['nullable', 'array'],
            'category_ids.*' => ['exists:categories,id'],
        ]);

        try {
            $isbnVo = new ISBN($validated['isbn']);
        } catch (\InvalidArgumentException $e) {
            return back()->withInput()->withErrors(['isbn' => $e->getMessage()]);
        }

        $book = Book::create([
            'isbn' => $isbnVo->getValue(),
            'title' => $validated['title'],
            'slug' => Str::slug($validated['title']) . '-' . rand(100, 999),
            'author' => $validated['author'],
            'publisher' => $validated['publisher'] ?? null,
            'description' => $validated['description'] ?? null,
            'stock' => $validated['stock'],
            'is_active' => true,
        ]);

        if (!empty($validated['category_ids'])) {
            $syncData = [];
            foreach ($validated['category_ids'] as $catId) {
                $syncData[$catId] = ['added_at' => now()];
            }
            $book->categories()->sync($syncData);
        }

        return redirect()->route('library.books.index')
            ->with('success', "Buku '{$book->title}' berhasil ditambahkan dengan ISBN valid.");
    }

    /**
     * Soft delete buku (audit trail).
     */
    public function destroy(Book $book)
    {
        $title = $book->title;
        $book->delete();

        return redirect()->route('library.books.index')
            ->with('success', "Buku '{$title}' dipindahkan ke Trash (Soft Delete).");
    }

    /**
     * Menampilkan daftar buku terhapus khusus Admin.
     */
    public function trash()
    {
        $trashedBooks = Book::onlyTrashed()->with('categories')->latest('deleted_at')->paginate(10);
        return view('library.books.trash', compact('trashedBooks'));
    }

    /**
     * Mengembalikan buku terhapus (Restore oleh Admin).
     */
    public function restore(int $id)
    {
        $book = Book::onlyTrashed()->findOrFail($id);
        $book->restore();

        return redirect()->route('library.books.trash')
            ->with('success', "Buku '{$book->title}' berhasil di-restore oleh Admin.");
    }
}
