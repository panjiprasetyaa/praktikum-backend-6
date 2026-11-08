<?php

namespace Modules\Circulation\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\SoftDeletes;
use Illuminate\Database\Eloquent\Relations\HasMany;
use Illuminate\Database\Eloquent\Relations\BelongsTo;
use Illuminate\Database\Eloquent\Builder;
use Modules\Membership\Models\Member;

class Loan extends Model
{
    use SoftDeletes;

    protected $fillable = [
        'loan_code',
        'member_id',
        'borrowed_at',
        'due_date',
        'returned_at',
        'status',
        'notes',
    ];

    protected $casts = [
        'borrowed_at' => 'datetime',
        'due_date' => 'datetime',
        'returned_at' => 'datetime',
    ];

    /**
     * Relasi HasMany ke detail item peminjaman.
     */
    public function details(): HasMany
    {
        return $this->hasMany(LoanDetail::class);
    }

    /**
     * Relasi HasMany ke data denda.
     */
    public function fines(): HasMany
    {
        return $this->hasMany(Fine::class);
    }

    /**
     * Relasi BelongsTo ke Anggota (Membership Context).
     */
    public function member(): BelongsTo
    {
        return $this->belongsTo(Member::class);
    }

    public function scopeBorrowed(Builder $query): Builder
    {
        return $query->where('status', 'borrowed');
    }

    public function scopeOverdue(Builder $query): Builder
    {
        return $query->where('status', 'borrowed')
                     ->where('due_date', '<', now());
    }

    public function scopeRecent(Builder $query, int $days = 30): Builder
    {
        return $query->where('borrowed_at', '>=', now()->subDays($days));
    }
}
