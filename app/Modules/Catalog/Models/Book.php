<?php

namespace Modules\Catalog\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\SoftDeletes;
use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\Eloquent\Relations\BelongsToMany;

class Book extends Model
{
    use SoftDeletes;

    protected $fillable = [
        'isbn',
        'title',
        'slug',
        'author',
        'publisher',
        'description',
        'stock',
        'is_active',
    ];

    protected $casts = [
        'stock' => 'integer',
        'is_active' => 'boolean',
    ];

    /**
     * Relasi Many-to-Many ke Kategori dengan pivot added_at.
     */
    public function categories(): BelongsToMany
    {
        return $this->belongsToMany(Category::class, 'book_category')
            ->withPivot('added_at');
    }

    /**
     * Query Scope: Hanya buku aktif yang memiliki stok > 0.
     */
    public function scopeAvailable(Builder $query): Builder
    {
        return $query->where('is_active', true)->where('stock', '>', 0);
    }

    /**
     * Query Scope: Pencarian buku berdasarkan judul, pengarang, deskripsi, atau ISBN.
     */
    public function scopeSearch(Builder $query, string $keyword): Builder
    {
        return $query->where(function (Builder $q) use ($keyword) {
            $q->where('title', 'like', "%{$keyword}%")
              ->orWhere('author', 'like', "%{$keyword}%")
              ->orWhere('isbn', 'like', "%{$keyword}%")
              ->orWhere('description', 'like', "%{$keyword}%");
        });
    }

    /**
     * Query Scope: Filter buku berdasarkan ID kategori.
     */
    public function scopeByCategory(Builder $query, int $categoryId): Builder
    {
        return $query->whereHas('categories', function (Builder $q) use ($categoryId) {
            $q->where('categories.id', $categoryId);
        });
    }

    /**
     * Query Scope: Buku dengan stok rendah.
     */
    public function scopeLowStock(Builder $query, int $threshold = 2): Builder
    {
        return $query->where('stock', '<=', $threshold);
    }

    /**
     * Memeriksa apakah stok mencukupi untuk jumlah peminjaman tertentu.
     */
    public function isInStock(int $quantity = 1): bool
    {
        return $this->is_active && $this->stock >= $quantity;
    }
}
