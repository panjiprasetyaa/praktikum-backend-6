<?php

namespace Modules\Membership\Providers;

use Illuminate\Support\ServiceProvider;
use Modules\Shared\Contracts\MemberServiceInterface;
use Modules\Membership\Services\MemberService;

class MembershipServiceProvider extends ServiceProvider
{
    public function register(): void
    {
        $this->app->bind(MemberServiceInterface::class, MemberService::class);
    }

    public function boot(): void
    {
        $this->loadMigrationsFrom(__DIR__ . '/../Migrations');
        $this->loadRoutesFrom(__DIR__ . '/../routes/web.php');
    }
}
