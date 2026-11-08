<?php

namespace Database\Seeders;

use Illuminate\Database\Seeder;
use Illuminate\Support\Str;
use Modules\Catalog\Models\Book;
use Modules\Catalog\Models\Category;
use Modules\Membership\Models\Member;
use Modules\Membership\Models\Role;

class LibrarySeeder extends Seeder
{
    public function run(): void
    {
        // 1. Roles
        $adminRole = Role::firstOrCreate(['slug' => 'admin'], [
            'name' => 'Administrator Perpustakaan',
            'description' => 'Memiliki akses penuh untuk mengelola buku, anggota, dan restore data soft deletes.',
        ]);

        $staffRole = Role::firstOrCreate(['slug' => 'staff'], [
            'name' => 'Staf Sirkulasi',
            'description' => 'Mengelola transaksi peminjaman, pengembalian, dan denda.',
        ]);

        $memberRole = Role::firstOrCreate(['slug' => 'member'], [
            'name' => 'Anggota Reguler',
            'description' => 'Mahasiswa atau dosen peminjam buku.',
        ]);

        // 2. Members
        $member1 = Member::firstOrCreate(['member_code' => 'MBR-2026-001'], [
            'name' => 'Panji Prasetya',
            'email' => 'panji@example.com',
            'phone' => '081234567890',
            'status' => 'active',
            'max_loans' => 5,
        ]);
        $member1->roles()->sync([$memberRole->id]);

        $member2 = Member::firstOrCreate(['member_code' => 'MBR-2026-002'], [
            'name' => 'Budi Santoso',
            'email' => 'budi@example.com',
            'phone' => '082345678901',
            'status' => 'active',
            'max_loans' => 3,
        ]);
        $member2->roles()->sync([$memberRole->id]);

        $memberSuspended = Member::firstOrCreate(['member_code' => 'MBR-2026-003'], [
            'name' => 'Siti Aminah',
            'email' => 'siti@example.com',
            'phone' => '083456789012',
            'status' => 'suspended', // Untuk uji validasi member tidak aktif
            'max_loans' => 3,
        ]);
        $memberSuspended->roles()->sync([$memberRole->id]);

        // 3. Hierarchical Categories (Self-Referencing)
        $tech = Category::firstOrCreate(['slug' => 'teknologi'], [
            'name' => 'Teknologi & Komputer',
            'description' => 'Buku seputar rekayasa perangkat lunak dan IT.',
            'parent_id' => null,
        ]);

        $science = Category::firstOrCreate(['slug' => 'sains'], [
            'name' => 'Sains & Matematika',
            'description' => 'Buku sains murni dan terapan.',
            'parent_id' => null,
        ]);

        $subProg = Category::firstOrCreate(['slug' => 'pemrograman'], [
            'name' => 'Pemrograman & Algoritma',
            'description' => 'Bahasa pemrograman, arsitektur backend, dan clean code.',
            'parent_id' => $tech->id,
        ]);

        $subAI = Category::firstOrCreate(['slug' => 'kecerdasan-buatan'], [
            'name' => 'Kecerdasan Buatan',
            'description' => 'Machine learning, data science, dan deep learning.',
            'parent_id' => $tech->id,
        ]);

        $subFisika = Category::firstOrCreate(['slug' => 'fisika'], [
            'name' => 'Fisika Terapan',
            'description' => 'Mekanika dan fisika komputasi.',
            'parent_id' => $science->id,
        ]);

        // 4. Books (dengan ISBN valid)
        $booksData = [
            [
                'isbn' => '978-0-13-235088-4',
                'title' => 'Clean Code: A Handbook of Agile Software Craftsmanship',
                'slug' => 'clean-code',
                'author' => 'Robert C. Martin',
                'publisher' => 'Prentice Hall',
                'description' => 'Panduan praktik terbaik penulisan kode yang rapi dan terawat.',
                'stock' => 5,
                'is_active' => true,
                'categories' => [$tech->id, $subProg->id],
            ],
            [
                'isbn' => '978-0-321-12521-7',
                'title' => 'Domain-Driven Design: Tackling Complexity in the Heart of Software',
                'slug' => 'domain-driven-design',
                'author' => 'Eric Evans',
                'publisher' => 'Addison-Wesley',
                'description' => 'Buku fundamental mengenai pendekatan DDD, Bounded Context, dan Ubiquitous Language.',
                'stock' => 3,
                'is_active' => true,
                'categories' => [$tech->id, $subProg->id],
            ],
            [
                'isbn' => '978-0-13-449416-6',
                'title' => 'Clean Architecture: A Craftsman\'s Guide to Software Structure and Design',
                'slug' => 'clean-architecture',
                'author' => 'Robert C. Martin',
                'publisher' => 'Prentice Hall',
                'description' => 'Prinsip arsitektur perangkat lunak yang scalable dan modular.',
                'stock' => 4,
                'is_active' => true,
                'categories' => [$tech->id, $subProg->id],
            ],
            [
                'isbn' => '978-0-201-63361-0',
                'title' => 'Design Patterns: Elements of Reusable Object-Oriented Software',
                'slug' => 'design-patterns',
                'author' => 'Erich Gamma, Richard Helm, Ralph Johnson, John Vlissides',
                'publisher' => 'Addison-Wesley',
                'description' => 'Pola desain perangkat lunak berorientasi objek yang dapat digunakan kembali.',
                'stock' => 2,
                'is_active' => true,
                'categories' => [$tech->id, $subProg->id],
            ],
            [
                'isbn' => '978-0-13-597444-5',
                'title' => 'The Pragmatic Programmer: Your Journey To Mastery',
                'slug' => 'pragmatic-programmer',
                'author' => 'David Thomas, Andrew Hunt',
                'publisher' => 'Addison-Wesley',
                'description' => 'Wawasan filosofis dan teknis bagi pengembang perangkat lunak profesional.',
                'stock' => 0, // STOK KOSONG (Khusus untuk pengujian Rollback Database Transaction)
                'is_active' => true,
                'categories' => [$tech->id, $subProg->id],
            ],
        ];

        foreach ($booksData as $data) {
            $catIds = $data['categories'];
            unset($data['categories']);

            $book = Book::firstOrCreate(['isbn' => $data['isbn']], $data);

            // Relasi Many-to-Many dengan Pivot timestamp added_at
            $syncData = [];
            foreach ($catIds as $catId) {
                $syncData[$catId] = ['added_at' => now()];
            }
            $book->categories()->syncWithoutDetaching($syncData);
        }
    }
}
