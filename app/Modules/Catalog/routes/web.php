<?php

use Illuminate\Support\Facades\Route;
use Modules\Catalog\Controllers\BookController;

Route::middleware(['web', 'auth'])->prefix('library')->name('library.')->group(function () {
    Route::get('/books', [BookController::class, 'index'])->name('books.index');
    Route::get('/books/create', [BookController::class, 'create'])->name('books.create');
    Route::post('/books', [BookController::class, 'store'])->name('books.store');
    Route::delete('/books/{book}', [BookController::class, 'destroy'])->name('books.destroy');

    // Fitur Restore Khusus Admin
    Route::middleware('role:admin')->group(function () {
        Route::get('/books/trash', [BookController::class, 'trash'])->name('books.trash');
        Route::post('/books/{id}/restore', [BookController::class, 'restore'])->name('books.restore');
    });
});
