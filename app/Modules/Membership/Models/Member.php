<?php

namespace Modules\Membership\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\SoftDeletes;
use Illuminate\Database\Eloquent\Relations\BelongsToMany;

class Member extends Model
{
    use SoftDeletes;

    protected $fillable = [
        'member_code',
        'name',
        'email',
        'phone',
        'status',
        'max_loans',
    ];

    protected $casts = [
        'max_loans' => 'integer',
    ];

    public function roles(): BelongsToMany
    {
        return $this->belongsToMany(Role::class, 'member_role');
    }

    public function canBorrow(): bool
    {
        return $this->status === 'active';
    }
}
