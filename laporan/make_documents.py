import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), fill_hex)
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def add_code_block(doc, code_text):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    set_cell_background(cell, "F4F4F4")
    set_cell_margins(cell, top=140, bottom=140, left=200, right=200)
    cell.width = Inches(6.5)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.15
    run = p.add_run(code_text)
    run.font.name = 'Consolas'
    run.font.size = Pt(8.5)
    run.font.color.rgb = RGBColor(30, 30, 30)
    doc.add_paragraph().paragraph_format.space_after = Pt(4)

doc = Document()

# Set Standard Margins (1 inch / 2.54 cm)
for section in doc.sections:
    section.top_margin = Inches(1)
    section.bottom_margin = Inches(1)
    section.left_margin = Inches(1)
    section.right_margin = Inches(1)

# Default style
style = doc.styles['Normal']
style.font.name = 'Times New Roman'
style.font.size = Pt(11)
style.font.color.rgb = RGBColor(0, 0, 0)

# ==============================================================================
# COVER PAGE
# ==============================================================================
title_p = doc.add_paragraph()
title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
title_p.paragraph_format.space_before = Pt(36)
title_p.paragraph_format.space_after = Pt(12)

r_main = title_p.add_run("LAPORAN PRAKTIKUM BACKEND DEVELOPMENT\n")
r_main.font.size = Pt(16)
r_main.font.bold = True

r_sub = title_p.add_run("PERTEMUAN KE-6: PENGELOLAAN DATA LANJUTAN DENGAN\nMODULAR MONOLITH & DOMAIN-DRIVEN DESIGN (DDD)\n")
r_sub.font.size = Pt(13)
r_sub.font.bold = True

r_case = title_p.add_run("\nSTUDI KASUS: SISTEM PERPUSTAKAAN MODULAR\n(CATALOG, MEMBERSHIP, DAN CIRCULATION CONTEXT)\n")
r_case.font.size = Pt(12)
r_case.font.bold = True

doc.add_paragraph().paragraph_format.space_after = Pt(60)

meta_p = doc.add_paragraph()
meta_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
meta_p.paragraph_format.line_spacing = 1.3

r_meta = meta_p.add_run(
    "Mata Kuliah : Backend Development (DT199)\n"
    "Program Studi : D4 / S1 Teknik Informatika & Sistem Informasi\n"
    "Dosen Pengampu : Tim Dosen Backend Development\n\n\n"
    "Disusun Oleh:\n"
    "Nama Mahasiswa : Panji Prasetya\n"
    "Tautan Repository GitHub :\n"
    "https://github.com/panjiprasetyaa/praktikum-backend-6.git\n\n\n"
    "TAHUN AKADEMIK 2026/2027"
)
r_meta.font.size = Pt(11)

doc.add_page_break()

# Helper for Headings
def add_h1(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(16)
    p.paragraph_format.space_after = Pt(6)
    r = p.add_run(text)
    r.font.name = 'Times New Roman'
    r.font.size = Pt(14)
    r.font.bold = True
    return p

def add_h2(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(4)
    r = p.add_run(text)
    r.font.name = 'Times New Roman'
    r.font.size = Pt(12)
    r.font.bold = True
    return p

def add_body(text, space_after=6):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.2
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    r = p.add_run(text)
    r.font.name = 'Times New Roman'
    r.font.size = Pt(11)
    return p

# ==============================================================================
# BAB I: PENDAHULUAN
# ==============================================================================
add_h1("BAB I: PENDAHULUAN")

add_h2("1.1 Latar Belakang")
add_body(
    "Dalam lanskap rekayasa perangkat lunak enterprise modern, arsitektur monolitik tradisional sering kali "
    "mengalami penurunan keterawatan (maintainability) dan tingginya keterikatan (high coupling) seiring bertambahnya "
    "fitur aplikasi. Pendekatan Modular Monolith yang dikombinasikan dengan prinsip Domain-Driven Design (DDD) "
    "menawarkan solusi elegan: mempertahankan kemudahan operasional dan deployment sistem monolitik, sembari "
    "memberlakukan batas domain (Bounded Context) yang tegas sebagaimana arsitektur microservices."
)
add_body(
    "Pada praktikum Pertemuan ke-6 mata kuliah Backend Development (DT199), mahasiswa ditantang untuk menerapkan "
    "teknik-teknik pengelolaan data tingkat lanjut menggunakan framework Laravel 13. Topik utama yang dipelajari "
    "mencakup relasi Eloquent lanjutan (Many-to-Many dengan pivot custom, Self-referencing hierarkis, HasMany), "
    "optimasi performa query database melalui Eager Loading guna mengatasi degradasi performa akibat masalah N+1 Query, "
    "penjaminan konsistensi data atomik menggunakan Database Transaction dengan penanganan rollback otomatis, "
    "mekanisme Soft Deletes untuk menjaga audit trail historis, perancangan Value Objects yang immutable, "
    "serta pemanfaatan Domain Events untuk komunikasi nir-kopling (decoupled communication) antar modul."
)

add_h2("1.2 Maksud dan Tujuan")
add_body("Adapun tujuan dari pelaksanaan praktikum ini adalah agar mahasiswa mampu:")
add_body("1. Menjelaskan dan merancang konsep Domain-Driven Design (DDD) serta Bounded Context dalam arsitektur Modular Monolith.")
add_body("2. Mengimplementasikan berbagai relasi Eloquent lanjutan: Many-to-Many dengan kolom pivot 'added_at', Self-referencing (Category induk ke sub-kategori), dan relasi agregat HasMany.")
add_body("3. Menerapkan teknik Eager Loading untuk mengeliminasi masalah N+1 Query dan membangun Query Scopes yang reusable.")
add_body("4. Mengimplementasikan Database Transaction (DB::transaction) untuk menjamin atomisitas transaksi, serta membuktikan berjalannya rollback saat terjadi kegagalan invariant bisnis.")
add_body("5. Menerapkan Soft Deletes dan fungsi restore data terhapus untuk kebutuhan audit trail sistem.")
add_body("6. Merancang Value Object (ISBN dan Denda) yang memvalidasi format data dan menghitung denda keterlambatan secara otomatis.")
add_body("7. Menerapkan Domain Event (BookBorrowed) dan Listener guna menjaga integritas batas antar konteks tanpa ketergantungan langsung.")

add_h2("1.3 Ruang Lingkup Studi Kasus: Sistem Perpustakaan Modular")
add_body(
    "Studi kasus yang dikerjakan adalah Sistem Informasi Perpustakaan Modular yang terbagi secara independen menjadi "
    "tiga Bounded Context utama dan satu Shared Kernel:\n"
    "a. Catalog Context: Bertanggung jawab mengelola katalog buku, pengarang, penerbit, serta hierarki kategori buku.\n"
    "b. Membership Context: Bertanggung jawab mengelola data anggota perpustakaan, hak akses (roles), serta status keanggotaan.\n"
    "c. Circulation Context: Bertanggung jawab memproses peminjaman buku, snapshot data historis, pencatatan keterlambatan, pengembalian, dan penghitungan denda.\n"
    "d. Shared Kernel: Berisi kontrak antarmuka (interfaces/contracts), Value Objects umum, dan custom domain exceptions yang dibagi pakai antar modul secara terkontrol."
)

# ==============================================================================
# BAB II: PERANCANGAN
# ==============================================================================
add_h1("BAB II: PERANCANGAN ARSITEKTUR DAN BASIS DATA")

add_h2("2.1 Konsep Bounded Context & Shared Kernel")
add_body(
    "Prinsip inti Domain-Driven Design menyatakan bahwa setiap konteks domain harus memiliki Ubiquitous Language "
    "dan model datanya sendiri. Modul Sirkulasi tidak diizinkan mengakses model Eloquent atau tabel database milik "
    "Katalog secara langsung, melainkan harus berkomunikasi melalui abstraksi Contract (Interface) di Shared Kernel. "
    "Berikut adalah arsitektur Bounded Context sistem perpustakaan modular:"
)

# Image 1: Bounded Context
p_img1 = doc.add_paragraph()
p_img1.alignment = WD_ALIGN_PARAGRAPH.CENTER
r_img1 = p_img1.add_run()
img1_path = r"d:\project6\laporan\images\diagram_bounded_context_bw.png"
if os.path.exists(img1_path):
    r_img1.add_picture(img1_path, width=Inches(6.0))
p_cap1 = doc.add_paragraph()
p_cap1.alignment = WD_ALIGN_PARAGRAPH.CENTER
r_cap1 = p_cap1.add_run("Gambar 2.1 Diagram Bounded Context dan Shared Kernel (Format Monochrome)")
r_cap1.font.size = Pt(9.5)
r_cap1.font.italic = True

add_h2("2.2 Penjelasan Aggregate Root dan Invariant Bisnis")
add_body(
    "Aggregate adalah kumpulan objek domain (Entities dan Value Objects) yang diperlakukan sebagai satu unit transaksi. "
    "Setiap aggregate dipimpin oleh Aggregate Root yang bertanggung jawab memvalidasi dan memelihara Invariant (aturan bisnis)."
)

# Table Aggregate
tbl_agg = doc.add_table(rows=4, cols=4)
tbl_agg.alignment = WD_TABLE_ALIGNMENT.CENTER
headers_agg = ["Bounded Context", "Aggregate Root", "Entities di Dalamnya", "Invariant (Aturan Bisnis)"]
for col_idx, h in enumerate(headers_agg):
    cell = tbl_agg.cell(0, col_idx)
    set_cell_background(cell, "E0E0E0")
    set_cell_margins(cell, top=120, bottom=120, left=150, right=150)
    p = cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(h)
    r.font.bold = True
    r.font.size = Pt(9.5)

agg_data = [
    ("Catalog Context", "Book (Buku)", "Category, Author, Publisher", "Stok buku tidak boleh bernilai negatif; ISBN harus valid 10 atau 13 digit; Hanya buku aktif yang dapat dipinjam."),
    ("Membership Context", "Member (Anggota)", "Role", "Email dan kode anggota harus unik; Peminjaman hanya dizinkan untuk anggota dengan status 'active'."),
    ("Circulation Context", "Loan (Peminjaman)", "LoanDetail, Fine (Denda)", "Peminjaman wajib memotong stok buku; Detail wajib menyimpan snapshot data buku; Denda dihitung otomatis Rp 2.000/hari.")
]

for row_idx, data in enumerate(agg_data, start=1):
    for col_idx, val in enumerate(data):
        cell = tbl_agg.cell(row_idx, col_idx)
        set_cell_background(cell, "FFFFFF" if row_idx % 2 != 0 else "F9F9F9")
        set_cell_margins(cell, top=100, bottom=100, left=150, right=150)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        r = p.add_run(val)
        r.font.size = Pt(9)

doc.add_paragraph().paragraph_format.space_after = Pt(8)

add_h2("2.3 Pemetaan Relasi Antar Tabel dan Snapshot Pattern")
add_body(
    "Desain relasi database pada aplikasi ini mengimplementasikan prinsip-prinsip berikut:\n"
    "1. Many-to-Many dengan Pivot: Relasi antara buku dan kategori melalui tabel pivot 'book_category' yang memuat timestamp 'added_at'.\n"
    "2. Self-Referencing: Tabel 'categories' memiliki foreign key 'parent_id' yang merujuk pada tabel itu sendiri untuk mendukung sub-kategori berjenjang.\n"
    "3. HasMany Aggregate: Relasi 'loans' ke 'loan_details' bersifat One-to-Many dalam batas agregat peminjaman.\n"
    "4. Snapshot Pattern: Pada tabel 'loan_details', kolom 'book_title' dan 'book_isbn' disimpan secara terduplikasi pada saat transaksi peminjaman terjadi. Pola ini menjamin bahwa perubahan judul atau perbaikan data master buku di kemudian hari tidak akan merusak keaslian bukti riwayat transaksi peminjaman masa lalu."
)

# Image 2: ERD
p_img2 = doc.add_paragraph()
p_img2.alignment = WD_ALIGN_PARAGRAPH.CENTER
r_img2 = p_img2.add_run()
img2_path = r"d:\project6\laporan\images\diagram_erd_bw.png"
if os.path.exists(img2_path):
    r_img2.add_picture(img2_path, width=Inches(6.2))
p_cap2 = doc.add_paragraph()
p_cap2.alignment = WD_ALIGN_PARAGRAPH.CENTER
r_cap2 = p_cap2.add_run("Gambar 2.2 Entity Relationship Diagram (ERD) Sistem Perpustakaan (Format Monochrome)")
r_cap2.font.size = Pt(9.5)
r_cap2.font.italic = True

add_h2("2.4 Alur Database Transaction dan Mekanisme Auto-Rollback")
add_body(
    "Operasi peminjaman buku menuntut integritas data yang tinggi: pengecekan kelayakan anggota, validasi stok buku, "
    "pembuatan header pinjaman, pencatatan snapshot detail, pemotongan stok pada katalog, hingga penembakan event notifikasi "
    "harus berlangsung secara atomik (All or Nothing). Jika salah satu buku yang diminta tidak memiliki stok yang cukup, "
    "sistem wajib melempar InsufficientStockException sehingga transaksi dibatalkan seketika tanpa ada perubahan status di database."
)

# Image 3: Transaction Flow
p_img3 = doc.add_paragraph()
p_img3.alignment = WD_ALIGN_PARAGRAPH.CENTER
r_img3 = p_img3.add_run()
img3_path = r"d:\project6\laporan\images\diagram_transaction_flow_bw.png"
if os.path.exists(img3_path):
    r_img3.add_picture(img3_path, width=Inches(4.8))
p_cap3 = doc.add_paragraph()
p_cap3.alignment = WD_ALIGN_PARAGRAPH.CENTER
r_cap3 = p_cap3.add_run("Gambar 2.3 Flowchart Database Transaction dan Mekanisme Rollback (Format Monochrome)")
r_cap3.font.size = Pt(9.5)
r_cap3.font.italic = True

doc.add_page_break()

# ==============================================================================
# BAB III: IMPLEMENTASI
# ==============================================================================
add_h1("BAB III: IMPLEMENTASI SISTEM")

add_h2("3.1 Struktur Direktori Modular Monolith")
add_body(
    "Sistem diorganisasikan ke dalam direktori modul pada app/Modules/. Struktur ini memisahkan model, "
    "migrasi, service provider, service, serta events per Bounded Context:"
)
code_dir = (
    "app/Modules/\n"
    "├── Catalog/\n"
    "│   ├── Migrations/\n"
    "│   │   ├── 2026_11_08_000001_create_categories_table.php\n"
    "│   │   ├── 2026_11_08_000002_create_books_table.php\n"
    "│   │   └── 2026_11_08_000003_create_book_category_table.php\n"
    "│   ├── Models/ (Book.php, Category.php)\n"
    "│   ├── Providers/ (CatalogServiceProvider.php)\n"
    "│   └── Services/ (CatalogService.php)\n"
    "├── Membership/\n"
    "│   ├── Migrations/ (create_members_and_roles_table.php)\n"
    "│   ├── Models/ (Member.php, Role.php)\n"
    "│   ├── Providers/ (MembershipServiceProvider.php)\n"
    "│   └── Services/ (MemberService.php)\n"
    "├── Circulation/\n"
    "│   ├── Events/ (BookBorrowed.php)\n"
    "│   ├── Listeners/ (LogBookBorrowedActivity.php)\n"
    "│   ├── Migrations/ (create_loans_details_fines_table.php)\n"
    "│   ├── Models/ (Loan.php, LoanDetail.php, Fine.php)\n"
    "│   ├── Providers/ (CirculationServiceProvider.php)\n"
    "│   └── Services/ (CirculationService.php)\n"
    "└── Shared/\n"
    "    ├── Contracts/ (BookServiceInterface.php, MemberServiceInterface.php)\n"
    "    ├── Exceptions/ (InsufficientStockException.php, MemberNotEligibleException.php)\n"
    "    └── ValueObjects/ (ISBN.php, Denda.php)"
)
add_code_block(doc, code_dir)

add_h2("3.2 Implementasi Shared Kernel (Value Objects & Contracts)")
add_body(
    "Value Object 'ISBN' memastikan bahwa setiap nomor buku yang masuk divalidasi keabsahannya berdasarkan algoritma "
    "ISBN-10 maupun ISBN-13 (check digit checksum):"
)
code_isbn = (
    "namespace Modules\\Shared\\ValueObjects;\n\n"
    "class ISBN {\n"
    "    private string $value;\n"
    "    public function __construct(string $value) {\n"
    "        $cleaned = preg_replace('/[^0-9X]/i', '', $value);\n"
    "        if (!$this->isValid($cleaned)) {\n"
    "            throw new \\InvalidArgumentException(\"Format ISBN tidak valid: {$value}\");\n"
    "        }\n"
    "        $this->value = strtoupper(trim($value));\n"
    "    }\n"
    "    // ... method validasi check-digit checksum 10 dan 13 digit\n"
    "}"
)
add_code_block(doc, code_isbn)

add_body(
    "Value Object 'Denda' mengkapsulasi logika tarif denda harian dan penghitungan otomatis berdasarkan hari keterlambatan:"
)
code_denda = (
    "namespace Modules\\Shared\\ValueObjects;\n\n"
    "class Denda {\n"
    "    private int $daysOverdue;\n"
    "    private float $dailyRate;\n"
    "    private float $amount;\n\n"
    "    public function __construct(int $daysOverdue, float $dailyRate = 2000.0) {\n"
    "        if ($daysOverdue < 0) throw new \\InvalidArgumentException('Hari denda tidak boleh negatif');\n"
    "        $this->daysOverdue = $daysOverdue;\n"
    "        $this->dailyRate = $dailyRate;\n"
    "        $this->amount = $daysOverdue * $dailyRate;\n"
    "    }\n"
    "    public function formatRupiah(): string {\n"
    "        return 'Rp ' . number_format($this->amount, 0, ',', '.');\n"
    "    }\n"
    "}"
)
add_code_block(doc, code_denda)

add_h2("3.3 Implementasi Catalog Context (Relasi Lanjutan & Query Scopes)")
add_body(
    "Model 'Category' mengimplementasikan relasi Self-referencing hierarkis dan Many-to-Many ke buku dengan pivot 'added_at':"
)
code_cat = (
    "namespace Modules\\Catalog\\Models;\n"
    "use Illuminate\\Database\\Eloquent\\Model;\n"
    "use Illuminate\\Database\\Eloquent\\SoftDeletes;\n\n"
    "class Category extends Model {\n"
    "    use SoftDeletes;\n"
    "    protected $fillable = ['name', 'slug', 'description', 'parent_id'];\n\n"
    "    public function parent() { return $this->belongsTo(Category::class, 'parent_id'); }\n"
    "    public function children() { return $this->hasMany(Category::class, 'parent_id'); }\n"
    "    public function books() {\n"
    "        return $this->belongsToMany(Book::class, 'book_category')->withPivot('added_at');\n"
    "    }\n"
    "}"
)
add_code_block(doc, code_cat)

add_body(
    "Model 'Book' dilengkapi dengan Query Scopes (available, search, byCategory) dan trait SoftDeletes:"
)
code_book = (
    "namespace Modules\\Catalog\\Models;\n"
    "use Illuminate\\Database\\Eloquent\\Model;\n"
    "use Illuminate\\Database\\Eloquent\\SoftDeletes;\n"
    "use Illuminate\\Database\\Eloquent\\Builder;\n\n"
    "class Book extends Model {\n"
    "    use SoftDeletes;\n"
    "    public function scopeAvailable(Builder $query): Builder {\n"
    "        return $query->where('is_active', true)->where('stock', '>', 0);\n"
    "    }\n"
    "    public function scopeSearch(Builder $query, string $keyword): Builder {\n"
    "        return $query->where(function ($q) use ($keyword) {\n"
    "            $q->where('title', 'like', \"%{$keyword}%\")\n"
    "              ->orWhere('author', 'like', \"%{$keyword}%\")\n"
    "              ->orWhere('isbn', 'like', \"%{$keyword}%\");\n"
    "        });\n"
    "    }\n"
    "    public function scopeByCategory(Builder $query, int $categoryId): Builder {\n"
    "        return $query->whereHas('categories', fn($q) => $q->where('categories.id', $categoryId));\n"
    "    }\n"
    "}"
)
add_code_block(doc, code_book)

add_h2("3.4 Implementasi Circulation Context (Database Transaction & Snapshot)")
add_body(
    "Metode borrowBooks() pada CirculationService membungkus operasi peminjaman ke dalam DB::transaction(), "
    "memotong stok buku secara atomik lewat contract, menyimpan snapshot ke loan_details, serta menembakkan Domain Event:"
)
code_tx = (
    "public function borrowBooks(int $memberId, array $bookIds, int $loanDays = 7): Loan {\n"
    "    return DB::transaction(function () use ($memberId, $bookIds, $loanDays) {\n"
    "        if (!$this->memberService->canBorrow($memberId)) {\n"
    "            throw new MemberNotEligibleException('Member tidak aktif / melampaui kuota.');\n"
    "        }\n"
    "        $loan = Loan::create([\n"
    "            'loan_code' => 'LOAN-' . date('Ymd') . '-' . strtoupper(substr(uniqid(), -5)),\n"
    "            'member_id' => $memberId,\n"
    "            'borrowed_at' => now(),\n"
    "            'due_date' => now()->addDays($loanDays),\n"
    "            'status' => 'borrowed'\n"
    "        ]);\n"
    "        foreach ($bookIds as $bookId) {\n"
    "            $book = $this->bookService->getBookForLoan($bookId);\n"
    "            if (!$this->bookService->isStockAvailable($bookId, 1)) {\n"
    "                throw new InsufficientStockException($book['title'], $book['stock'], 1);\n"
    "            }\n"
    "            LoanDetail::create([\n"
    "                'loan_id' => $loan->id,\n"
    "                'book_id' => $bookId,\n"
    "                'book_title' => $book['title'], // SNAPSHOT\n"
    "                'book_isbn'  => $book['isbn'],  // SNAPSHOT\n"
    "            ]);\n"
    "            $this->bookService->reduceStock($bookId, 1);\n"
    "        }\n"
    "        event(new BookBorrowed($loan->load('details')));\n"
    "        return $loan->load('details');\n"
    "    });\n"
    "}"
)
add_code_block(doc, code_tx)

add_h2("3.5 Riwayat Commit Git (Version Control Evidence)")
add_body("Seluruh tahapan implementasi dicatat menggunakan riwayat commit Git yang terstruktur dan teratur:")

tbl_git = doc.add_table(rows=9, cols=3)
tbl_git.alignment = WD_TABLE_ALIGNMENT.CENTER
headers_git = ["Commit Hash", "Tipe & Pesan Commit", "Fungsi Modul yang Ditambahkan"]
for col_idx, h in enumerate(headers_git):
    cell = tbl_git.cell(0, col_idx)
    set_cell_background(cell, "E0E0E0")
    set_cell_margins(cell, top=120, bottom=120, left=150, right=150)
    p = cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(h)
    r.font.bold = True
    r.font.size = Pt(9.5)

commits_data = [
    ("b9d5b44", "chore: initialize laravel 13 project for praktikum backend 6", "Inisialisasi repositori Git dan konfigurasi sanitasi file AI."),
    ("466e7b2", "feat(shared): implement ISBN, Denda, exceptions, and contracts", "Pembangunan Shared Kernel: Value Objects, Exceptions, dan Interface."),
    ("d6054f3", "feat(catalog): implement books, hierarchical categories, and service", "Migrasi, Model Buku-Kategori (pivot added_at), dan CatalogService."),
    ("fa76089", "feat(membership): implement member models, roles, and service", "Migrasi, Model Anggota, Roles, dan MemberService."),
    ("7c8a5b4", "feat(circulation): implement borrow transactions and BookBorrowed event", "Migrasi Peminjaman, Detail Snapshot, Domain Event, dan Transaksi."),
    ("2c153af", "feat: register module service providers in bootstrap/providers.php", "Registrasi provider modul ke arsitektur Laravel 13."),
    ("58933bf", "feat(seeders): implement LibrarySeeder with books and members", "Seeding data uji realistis dengan ISBN-13 terverifikasi."),
    ("33a6185", "test: add automated feature tests and interactive library demo command", "Pembuatan test suite otomatis dan console command demonstrasi.")
]

for row_idx, data in enumerate(commits_data, start=1):
    for col_idx, val in enumerate(data):
        cell = tbl_git.cell(row_idx, col_idx)
        set_cell_background(cell, "FFFFFF" if row_idx % 2 != 0 else "F9F9F9")
        set_cell_margins(cell, top=80, bottom=80, left=150, right=150)
        p = cell.paragraphs[0]
        r = p.add_run(val)
        r.font.size = Pt(8.5)
        if col_idx == 0:
            r.font.name = 'Consolas'
            r.font.bold = True

doc.add_page_break()

# ==============================================================================
# BAB IV: PENGUJIAN
# ==============================================================================
add_h1("BAB IV: HASIL PENGUJIAN DAN ANALISIS")

add_h2("4.1 Pengujian Eliminasi Masalah N+1 Query (Query Optimization)")
add_body(
    "Masalah N+1 Query terjadi ketika perulangan data induk (N record) memicu eksekusi N buah query SQL tambahan "
    "untuk memuat relasinya. Dengan memanfaatkan Eager Loading (with(['details', 'member'])), seluruh relasi diambil "
    "hanya dalam 3 query gabungan konstan tanpa dipengaruhi besarnya jumlah data."
)

# Image 4: Query Chart
p_img4 = doc.add_paragraph()
p_img4.alignment = WD_ALIGN_PARAGRAPH.CENTER
r_img4 = p_img4.add_run()
img4_path = r"d:\project6\laporan\images\chart_query_comparison_bw.png"
if os.path.exists(img4_path):
    r_img4.add_picture(img4_path, width=Inches(5.5))
p_cap4 = doc.add_paragraph()
p_cap4.alignment = WD_ALIGN_PARAGRAPH.CENTER
r_cap4 = p_cap4.add_run("Gambar 4.1 Grafik Perbandingan Eksekusi Query Database (N+1 Query vs Eager Loading)")
r_cap4.font.size = Pt(9.5)
r_cap4.font.italic = True

tbl_n1 = doc.add_table(rows=3, cols=4)
tbl_n1.alignment = WD_TABLE_ALIGNMENT.CENTER
headers_n1 = ["Metode Pengambilan", "Jumlah Data Peminjaman", "Jumlah Query SQL", "Efisiensi Performa"]
for col_idx, h in enumerate(headers_n1):
    cell = tbl_n1.cell(0, col_idx)
    set_cell_background(cell, "E0E0E0")
    set_cell_margins(cell, top=100, bottom=100, left=150, right=150)
    p = cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(h)
    r.font.bold = True
    r.font.size = Pt(9)

n1_data = [
    ("Tanpa Eager Loading (Lazy Loading loop)", "5 Data Peminjaman", "11 Query SQL", "Boros Sumber Daya & Lambat (N+1 Query)"),
    ("Dengan Eager Loading with(['details', 'member'])", "5 Data Peminjaman", "3 Query SQL", "Sangat Efisien & Teroptimasi (Konstan)")
]
for row_idx, data in enumerate(n1_data, start=1):
    for col_idx, val in enumerate(data):
        cell = tbl_n1.cell(row_idx, col_idx)
        set_cell_margins(cell, top=80, bottom=80, left=150, right=150)
        p = cell.paragraphs[0]
        r = p.add_run(val)
        r.font.size = Pt(8.5)

doc.add_paragraph().paragraph_format.space_after = Pt(8)

add_h2("4.2 Pengujian Database Transaction & Verifikasi Rollback")
add_body(
    "Pengujian dilakukan dengan mencoba meminjam buku yang stoknya telah kosong ('The Pragmatic Programmer', stok: 0). "
    "Sistem mendeteksi kekurangan stok saat iterasi berlangsung dan melempar InsufficientStockException. "
    "Hasil verifikasi menunjukkan bahwa DB::transaction() segera melakukan rollback penuh, sehingga jumlah record "
    "tabel 'loans' dan 'loan_details' tidak mengalami penambahan sama sekali (data konsisten)."
)
code_rb_out = (
    "Mencoba meminjam buku dengan stok kosong ('The Pragmatic Programmer: Your Journey To Mastery', stok: 0)...\n"
    "[BERHASIL] Exception tertangkap: Stok buku 'The Pragmatic Programmer' tidak mencukupi. Tersedia: 0, diminta: 1.\n"
    "[VERIFIKASI ROLLBACK] Record Loan sebelum: 5, sesudah: 5\n"
    "-> DB::transaction() berhasil membatalkan seluruh operasi secara atomik! Konsistensi basis data terjaga 100%."
)
add_code_block(doc, code_rb_out)

add_h2("4.3 Pengujian Soft Deletes & Restore")
add_body(
    "Model 'Book' dan 'Member' diuji penghapusan datanya menggunakan delete(). Record tidak terhapus dari tabel secara fisik, "
    "melainkan ditandai dengan timestamp deleted_at. Pemanggilan method restore() mengembalikan status data menjadi aktif kembali:"
)
code_sd_out = (
    "Menghapus buku #1 ('Clean Code') secara Soft Delete...\n"
    "- Book::count() (Record Aktif)               : 4 Buku\n"
    "- Book::withTrashed()->count() (Total Fisik)  : 5 Buku\n"
    "Mengembalikan buku dengan restore()...\n"
    "- Book::count() setelah restore             : 5 Buku [DATA PULIH SEMPURNA]"
)
add_code_block(doc, code_sd_out)

add_h2("4.4 Pengujian Otomatis Feature Test Suite (Pest / PHPUnit)")
add_body(
    "Seluruh kriteria penilaian praktikum diuji secara otomatis melalui feature test suite "
    "'tests/Feature/LibraryModularDDDTest.php'. Hasil pengujian menunjukkan 100% lulus (6 passed, 38 assertions):"
)
code_test_out = (
    "PASS Tests\\Feature\\LibraryModularDDDTest\n"
    "✓ test_relasi_lanjutan (Many-to-Many pivot added_at, Self-referencing, HasMany)\n"
    "✓ test_query_optimization_dan_scopes (Eager loading with() dan Query Scopes)\n"
    "✓ test_database_transaction_dan_rollback (Atomisitas & Auto-rollback)\n"
    "✓ test_soft_deletes_dan_restore (Audit trail soft delete & restore)\n"
    "✓ test_domain_event_dispatched (Event BookBorrowed dipancarkan)\n"
    "✓ test_value_objects_isbn_dan_denda (Validasi ISBN & kalkulasi denda)\n\n"
    "Tests: 6 passed (38 assertions) | Execution Duration: 1.05s"
)
add_code_block(doc, code_test_out)

# ==============================================================================
# BAB V: KESIMPULAN
# ==============================================================================
add_h1("BAB V: KESIMPULAN")
add_body(
    "Berdasarkan perancangan, implementasi, dan pengujian yang telah dilakukan pada Sistem Perpustakaan Modular, "
    "dapat diambil kesimpulan sebagai berikut:\n\n"
    "1. Penerapan arsitektur Modular Monolith dengan Domain-Driven Design (DDD) berhasil memecah kompleksitas domain "
    "ke dalam Bounded Context yang jelas (Catalog, Membership, Circulation, dan Shared Kernel), sehingga mencegah "
    "terjadinya hidden coupling antar tabel dan memudahkan pemeliharaan kode jangka panjang.\n\n"
    "2. Relasi lanjutan Eloquent terbukti sangat fleksibel dalam memodelkan struktur bisnis riil: relasi Self-referencing "
    "efektif menangani kategori hierarkis, relasi Many-to-Many dengan kolom pivot 'added_at' mencatat metadata relasi, "
    "dan Snapshot Pattern pada detail peminjaman menjamin keutuhan data historis transaksi.\n\n"
    "3. Optimasi query melalui Eager Loading terbukti secara empiris berhasil menurunkan beban query database secara drastis "
    "(dari 11 query menjadi hanya 3 query konstan untuk 5 transaksi), meniadakan masalah N+1 Query yang lazim terjadi pada ORM.\n\n"
    "4. Penggunaan Database Transaction (DB::transaction) menjamin sifat ACID pada proses peminjaman buku: operasi pengurangan "
    "stok dan pembuatan record berhasil secara utuh, atau dibatalkan seutuhnya (auto-rollback) tanpa meninggalkan jejak data parsial "
    "saat terjadi pelanggaran invariant stok habis.\n\n"
    "5. Value Object (ISBN dan Denda) meningkatkan derajat 'Domain-Richness' pada aplikasi dengan menjamin immutabilitas dan "
    "validitas data sejak saat instansiasi dilakukan."
)

# ==============================================================================
# LAMPIRAN
# ==============================================================================
add_h1("LAMPIRAN: TAUTAN REPOSITORY GITHUB")
add_body("Seluruh kode sumber, riwayat commit, struktur modul, dan script pengujian praktikum ini dapat diakses secara publik pada:")
p_link = doc.add_paragraph()
r_link = p_link.add_run("🔗 https://github.com/panjiprasetyaa/praktikum-backend-6.git")
r_link.font.name = 'Consolas'
r_link.font.size = Pt(11)
r_link.font.bold = True

# Save Docx
docx_path = r"d:\project6\laporan\LAPORAN_PRAKTIKUM_PERTEMUAN_6.docx"
doc.save(docx_path)
print(f"Word document saved to: {docx_path}")
