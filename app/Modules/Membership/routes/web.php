<?php

use Illuminate\Support\Facades\Route;
use Modules\Membership\Controllers\MemberController;

Route::middleware(['web', 'auth'])->prefix('library')->name('library.')->group(function () {
    Route::get('/members', [MemberController::class, 'index'])->name('members.index');
    Route::post('/members', [MemberController::class, 'store'])->name('members.store');
    Route::delete('/members/{member}', [MemberController::class, 'destroy'])->name('members.destroy');

    // Fitur Restore Khusus Admin
    Route::middleware('role:admin')->group(function () {
        Route::get('/members/trash', [MemberController::class, 'trash'])->name('members.trash');
        Route::post('/members/{id}/restore', [MemberController::class, 'restore'])->name('members.restore');
    });
});
