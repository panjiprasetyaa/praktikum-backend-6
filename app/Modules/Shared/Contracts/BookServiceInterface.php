<?php

namespace Modules\Shared\Contracts;

interface BookServiceInterface
{
    /**
     * Mengambil detail ringkas buku untuk snapshot peminjaman.
     * @return array{id: int, isbn: string, title: string, stock: int}|null
     */
    public function getBookForLoan(int $bookId): ?array;

    /**
     * Memeriksa ketersediaan stok buku.
     */
    public function isStockAvailable(int $bookId, int $quantity = 1): bool;

    /**
     * Mengurangi stok buku secara atomik.
     */
    public function reduceStock(int $bookId, int $quantity = 1): bool;

    /**
     * Mengembalikan stok buku (misal saat pengembalian atau pembatalan).
     */
    public function restoreStock(int $bookId, int $quantity = 1): bool;
}
