<?php

namespace Modules\Shared\ValueObjects;

use InvalidArgumentException;

class Denda
{
    private int $daysOverdue;
    private float $dailyRate;
    private float $amount;

    public function __construct(int $daysOverdue, float $dailyRate = 2000.0)
    {
        if ($daysOverdue < 0) {
            throw new InvalidArgumentException("Hari keterlambatan tidak boleh negatif: {$daysOverdue}");
        }

        if ($dailyRate < 0) {
            throw new InvalidArgumentException("Tarif denda harian tidak boleh negatif: {$dailyRate}");
        }

        $this->daysOverdue = $daysOverdue;
        $this->dailyRate = $dailyRate;
        $this->amount = $daysOverdue * $dailyRate;
    }

    public static function fromDays(int $days, float $dailyRate = 2000.0): self
    {
        return new self($days, $dailyRate);
    }

    public function getDaysOverdue(): int
    {
        return $this->daysOverdue;
    }

    public function getDailyRate(): float
    {
        return $this->dailyRate;
    }

    public function getAmount(): float
    {
        return $this->amount;
    }

    public function isZero(): bool
    {
        return $this->amount === 0.0;
    }

    public function formatRupiah(): string
    {
        return 'Rp ' . number_format($this->amount, 0, ',', '.');
    }

    public function equals(Denda $other): bool
    {
        return $this->amount === $other->amount;
    }

    public function __toString(): string
    {
        return $this->formatRupiah();
    }
}
