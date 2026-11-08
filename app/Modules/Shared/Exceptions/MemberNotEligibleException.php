<?php

namespace Modules\Shared\Exceptions;

use Exception;

class MemberNotEligibleException extends Exception
{
    public function __construct(string $reason)
    {
        parent::__construct("Anggota tidak memenuhi syarat untuk meminjam: {$reason}");
    }
}
