<?php

namespace Modules\Circulation\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

class Fine extends Model
{
    protected $fillable = [
        'loan_id',
        'days_overdue',
        'daily_rate',
        'total_fine',
        'is_paid',
        'paid_at',
    ];

    protected $casts = [
        'days_overdue' => 'integer',
        'daily_rate' => 'decimal:2',
        'total_fine' => 'decimal:2',
        'is_paid' => 'boolean',
        'paid_at' => 'datetime',
    ];

    public function loan(): BelongsTo
    {
        return $this->belongsTo(Loan::class);
    }
}
