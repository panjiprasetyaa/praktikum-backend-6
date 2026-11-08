<?php

namespace Modules\Shared\Contracts;

interface MemberServiceInterface
{
    /**
     * Mengambil data anggota untuk kebutuhan peminjaman.
     * @return array{id: int, member_code: string, name: string, status: string, max_loans: int}|null
     */
    public function getMemberForLoan(int $memberId): ?array;

    /**
     * Memeriksa apakah anggota aktif dan diperbolehkan meminjam.
     */
    public function canBorrow(int $memberId): bool;
}
