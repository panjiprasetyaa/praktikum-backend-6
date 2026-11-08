<?php

namespace Modules\Membership\Services;

use Modules\Membership\Models\Member;
use Modules\Shared\Contracts\MemberServiceInterface;

class MemberService implements MemberServiceInterface
{
    public function getMemberForLoan(int $memberId): ?array
    {
        $member = Member::find($memberId);
        if (!$member) {
            return null;
        }

        return [
            'id' => $member->id,
            'member_code' => $member->member_code,
            'name' => $member->name,
            'status' => $member->status,
            'max_loans' => $member->max_loans,
        ];
    }

    public function canBorrow(int $memberId): bool
    {
        $member = Member::find($memberId);
        return $member && $member->canBorrow();
    }
}
