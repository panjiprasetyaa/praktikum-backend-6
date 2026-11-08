<?php

namespace Modules\Circulation\Providers;

use Illuminate\Support\ServiceProvider;
use Illuminate\Support\Facades\Event;
use Modules\Circulation\Events\BookBorrowed;
use Modules\Circulation\Listeners\LogBookBorrowedActivity;

class CirculationServiceProvider extends ServiceProvider
{
    public function register(): void
    {
        //
    }

    public function boot(): void
    {
        $this->loadMigrationsFrom(__DIR__ . '/../Migrations');

        // Mendaftarkan Domain Event & Listener
        Event::listen(
            BookBorrowed::class,
            LogBookBorrowedActivity::class
        );
    }
}
