<?php

namespace Modules\Shared\Exceptions;

use Exception;

class InsufficientStockException extends Exception
{
    public function __construct(
        public readonly string $bookTitle,
        public readonly int $availableStock,
        public readonly int $requestedQuantity = 1
    ) {
        parent::__construct(
            "Stok buku '{$bookTitle}' tidak mencukupi. Tersedia: {$availableStock}, diminta: {$requestedQuantity}."
        );
    }
}
