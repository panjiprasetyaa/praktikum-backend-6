<?php

namespace Modules\Shared\ValueObjects;

use InvalidArgumentException;

class ISBN
{
    private string $value;

    public function __construct(string $value)
    {
        $cleaned = preg_replace('/[^0-9X]/i', '', $value);

        if (!$this->isValid($cleaned)) {
            throw new InvalidArgumentException("Format ISBN tidak valid: {$value}");
        }

        $this->value = strtoupper(trim($value));
    }

    private function isValid(string $isbn): bool
    {
        $len = strlen($isbn);
        if ($len === 10) {
            return $this->validateIsbn10($isbn);
        } elseif ($len === 13) {
            return $this->validateIsbn13($isbn);
        }

        return false;
    }

    private function validateIsbn10(string $isbn): bool
    {
        $sum = 0;
        for ($i = 0; $i < 9; $i++) {
            if (!is_numeric($isbn[$i])) {
                return false;
            }
            $sum += ((int) $isbn[$i]) * (10 - $i);
        }

        $lastChar = $isbn[9];
        $sum += ($lastChar === 'X') ? 10 : ((int) $lastChar);

        return ($sum % 11) === 0;
    }

    private function validateIsbn13(string $isbn): bool
    {
        if (!ctype_digit($isbn)) {
            return false;
        }

        $sum = 0;
        for ($i = 0; $i < 12; $i++) {
            $sum += ((int) $isbn[$i]) * ($i % 2 === 0 ? 1 : 3);
        }

        $checkDigit = (10 - ($sum % 10)) % 10;
        return $checkDigit === ((int) $isbn[12]);
    }

    public function getValue(): string
    {
        return $this->value;
    }

    public function equals(ISBN $other): bool
    {
        return $this->value === $other->value;
    }

    public function __toString(): string
    {
        return $this->value;
    }
}
