<?php

namespace Modules\Catalog\Services;

use Modules\Catalog\Models\Book;
use Modules\Shared\Contracts\BookServiceInterface;

class CatalogService implements BookServiceInterface
{
    /**
     * Mengambil data buku untuk snapshot peminjaman.
     */
    public function getBookForLoan(int $bookId): ?array
    {
        $book = Book::find($bookId);
        if (!$book) {
            return null;
        }

        return [
            'id' => $book->id,
            'isbn' => $book->isbn,
            'title' => $book->title,
            'author' => $book->author,
            'stock' => $book->stock,
        ];
    }

    /**
     * Memeriksa ketersediaan stok buku.
     */
    public function isStockAvailable(int $bookId, int $quantity = 1): bool
    {
        $book = Book::find($bookId);
        return $book && $book->isInStock($quantity);
    }

    /**
     * Mengurangi stok buku secara atomik dengan lock.
     */
    public function reduceStock(int $bookId, int $quantity = 1): bool
    {
        $book = Book::lockForUpdate()->find($bookId);
        if (!$book || !$book->isInStock($quantity)) {
            return false;
        }

        $book->decrement('stock', $quantity);
        return true;
    }

    /**
     * Mengembalikan stok buku.
     */
    public function restoreStock(int $bookId, int $quantity = 1): bool
    {
        $book = Book::lockForUpdate()->find($bookId);
        if (!$book) {
            return false;
        }

        $book->increment('stock', $quantity);
        return true;
    }
}
