<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::create('loans', function (Blueprint $table) {
            $table->id();
            $table->string('loan_code')->unique();
            $table->foreignId('member_id')->constrained('members')->onDelete('cascade');
            $table->timestamp('borrowed_at')->useCurrent();
            $table->timestamp('due_date');
            $table->timestamp('returned_at')->nullable();
            $table->string('status')->default('borrowed'); // borrowed, returned, overdue
            $table->text('notes')->nullable();
            $table->timestamps();
            $table->softDeletes();
        });

        Schema::create('loan_details', function (Blueprint $table) {
            $table->id();
            $table->foreignId('loan_id')->constrained('loans')->onDelete('cascade');
            $table->unsignedBigInteger('book_id'); // Cross-context reference
            $table->string('book_title'); // Snapshot
            $table->string('book_isbn');  // Snapshot
            $table->timestamp('returned_at')->nullable();
            $table->timestamps();
        });

        Schema::create('fines', function (Blueprint $table) {
            $table->id();
            $table->foreignId('loan_id')->constrained('loans')->onDelete('cascade');
            $table->integer('days_overdue')->default(0);
            $table->decimal('daily_rate', 10, 2)->default(2000.00);
            $table->decimal('total_fine', 10, 2)->default(0.00);
            $table->boolean('is_paid')->default(false);
            $table->timestamp('paid_at')->nullable();
            $table->timestamps();
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('fines');
        Schema::dropIfExists('loan_details');
        Schema::dropIfExists('loans');
    }
};
