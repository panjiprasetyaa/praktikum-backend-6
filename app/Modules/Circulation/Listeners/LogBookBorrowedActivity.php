<?php

namespace Modules\Circulation\Listeners;

use Illuminate\Support\Facades\Log;
use Modules\Circulation\Events\BookBorrowed;

class LogBookBorrowedActivity
{
    public function handle(BookBorrowed $event): void
    {
        $loan = $event->loan;
        $bookTitles = $loan->details->pluck('book_title')->join(', ');

        Log::info(
            "[Domain Event] Peminjaman Baru Berhasil Dibuat: Kode {$loan->loan_code} " .
            "oleh Member ID #{$loan->member_id}. Buku dipinjam: [{$bookTitles}]. Jatuh tempo: {$loan->due_date->format('Y-m-d')}."
        );
    }
}
