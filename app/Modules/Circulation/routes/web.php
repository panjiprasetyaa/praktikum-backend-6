<?php

use Illuminate\Support\Facades\Route;
use Modules\Circulation\Controllers\LoanController;

Route::middleware(['web', 'auth'])->prefix('library')->name('library.')->group(function () {
    Route::get('/loans', [LoanController::class, 'index'])->name('loans.index');
    Route::post('/loans', [LoanController::class, 'store'])->name('loans.store');
    Route::post('/loans/{id}/return', [LoanController::class, 'returnLoan'])->name('loans.return');
    Route::delete('/loans/{loan}', [LoanController::class, 'destroy'])->name('loans.destroy');

    // Fitur Restore Khusus Admin
    Route::middleware('role:admin')->group(function () {
        Route::get('/loans/trash', [LoanController::class, 'trash'])->name('loans.trash');
        Route::post('/loans/{id}/restore', [LoanController::class, 'restore'])->name('loans.restore');
    });
});
