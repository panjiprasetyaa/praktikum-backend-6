import os
import subprocess
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_TAB_ALIGNMENT, WD_TAB_LEADER
from docx.enum.table import WD_TABLE_ALIGNMENT
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
    set_cell_background(cell, "F5F5F5")
    set_cell_margins(cell, top=120, bottom=120, left=180, right=180)
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

# ==============================================================================
# BUILD WORD (.DOCX)
# ==============================================================================
doc = Document()

# Set Standard Margins (1 inch)
for section in doc.sections:
    section.top_margin = Inches(1)
    section.bottom_margin = Inches(1)
    section.left_margin = Inches(1)
    section.right_margin = Inches(1)

style = doc.styles['Normal']
style.font.name = 'Times New Roman'
style.font.size = Pt(11)
style.font.color.rgb = RGBColor(0, 0, 0)

# --- COVER PAGE ---
p_title = doc.add_paragraph()
p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_title.paragraph_format.space_before = Pt(24)
p_title.paragraph_format.space_after = Pt(4)

r = p_title.add_run("LAPORAN PRAKTIKUM\n")
r.font.size = Pt(14)
r.font.bold = True

r = p_title.add_run("BACKEND DEVELOPMENT\n")
r.font.size = Pt(14)
r.font.bold = True

r = p_title.add_run("PENGELOLAAN DATA LANJUTAN\n")
r.font.size = Pt(13)
r.font.bold = True

r = p_title.add_run("MODULAR MONOLITH & DOMAIN-DRIVEN DESIGN (DDD)")
r.font.size = Pt(13)
r.font.bold = True

# Logo
logo_path = r"d:\project6\laporan\images\logo_amikom.png"
p_logo = doc.add_paragraph()
p_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_logo.paragraph_format.space_before = Pt(48)
p_logo.paragraph_format.space_after = Pt(48)
if os.path.exists(logo_path):
    p_logo.add_run().add_picture(logo_path, width=Inches(2.3))

# Dosen Pengampu & Mahasiswa
p_meta = doc.add_paragraph()
p_meta.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_meta.paragraph_format.line_spacing = 1.3
p_meta.paragraph_format.space_after = Pt(12)

r = p_meta.add_run("Dosen Pengampu:\n")
r.font.size = Pt(11)
r = p_meta.add_run("Hastari Utama, S.Kom., M.Cs.\n\n\n")
r.font.size = Pt(11.5)
r.font.bold = True

r = p_meta.add_run("Disusun Oleh:\n")
r.font.size = Pt(11)
r = p_meta.add_run("Nama Mahasiswa : Muhammad Imam Panji Prasetya\n")
r.font.size = Pt(11.5)
r.font.bold = True
r = p_meta.add_run("NIM : 25.01.5303\n")
r.font.size = Pt(11.5)
r.font.bold = True
r = p_meta.add_run("Kelas : D3 Teknik Informatika\n")
r.font.size = Pt(11.5)
r.font.bold = True

doc.add_page_break()

# --- DAFTAR ISI PAGE ---
p_toc_title = doc.add_paragraph()
p_toc_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_toc_title.paragraph_format.space_before = Pt(12)
p_toc_title.paragraph_format.space_after = Pt(20)
r_toc = p_toc_title.add_run("DAFTAR ISI")
r_toc.font.size = Pt(14)
r_toc.font.bold = True

toc_items = [
    ("BAB I: PENDAHULUAN", "1", True),
    ("  1.1 Latar Belakang", "1", False),
    ("  1.2 Maksud dan Tujuan Praktikum", "1", False),
    ("  1.3 Ruang Lingkup Sistem Perpustakaan Modular", "2", False),
    ("BAB II: PERANCANGAN SISTEM", "3", True),
    ("  2.1 Diagram Bounded Context dan Shared Kernel", "3", False),
    ("  2.2 Analisis Aggregate Root dan Invariant Bisnis", "4", False),
    ("  2.3 Entity Relationship Diagram (ERD) dan Snapshot Pattern", "5", False),
    ("  2.4 Diagram Alur Database Transaction dan Mekanisme Auto-Rollback", "6", False),
    ("BAB III: IMPLEMENTASI SISTEM", "7", True),
    ("  3.1 Struktur Direktori Bounded Context (Modular Monolith)", "7", False),
    ("  3.2 Implementasi Shared Kernel (Value Objects, Exceptions, Contracts)", "8", False),
    ("  3.3 Implementasi Catalog Context (Buku, Kategori Hierarkis, Pivot added_at)", "9", False),
    ("  3.4 Implementasi Membership Context (Anggota, Role, MemberService)", "10", False),
    ("  3.5 Implementasi Circulation Context (Peminjaman, Detail Snapshot, Denda)", "11", False),
    ("  3.6 Implementasi CirculationService dengan Database Transaction Atomik", "12", False),
    ("  3.7 Konfigurasi Service Provider di bootstrap/providers.php", "13", False),
    ("  3.8 Riwayat Commit Git (Conventional Commits)", "13", False),
    ("BAB IV: PENGUJIAN SISTEM", "14", True),
    ("  4.1 Pengujian Relasi Lanjutan (Self-Referencing & Many-to-Many Pivot)", "14", False),
    ("  4.2 Pengujian Query Optimization (Eliminasi Masalah N+1 Query)", "15", False),
    ("  4.3 Pengujian Query Scopes (Available, Search, ByCategory)", "16", False),
    ("  4.4 Pengujian Database Transaction Berhasil (Atomisitas Pemotongan Stok)", "17", False),
    ("  4.5 Pengujian Database Transaction Rollback (Stok Kosong)", "18", False),
    ("  4.6 Pengujian Soft Deletes dan Restore Data Terhapus", "19", False),
    ("  4.7 Pengujian Value Objects (ISBN & Kalkulasi Denda)", "20", False),
    ("  4.8 Pengujian Domain Event BookBorrowed & Listener Logging", "21", False),
    ("  4.9 Matriks Hasil Pengujian Otomatis (Automated Testing Pest / PHPUnit)", "22", False),
    ("BAB V: KESIMPULAN", "23", True),
    ("LAMPIRAN", "24", True)
]

for title, page, is_bold in toc_items:
    p = doc.add_paragraph()
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.tab_stops.add_tab_stop(Inches(6.5), WD_TAB_ALIGNMENT.RIGHT, WD_TAB_LEADER.DOTS)
    r = p.add_run(f"{title}\t{page}")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(10.5)
    r.font.bold = is_bold

doc.add_page_break()

# Helper Functions
def add_h1(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(18)
    p.paragraph_format.space_after = Pt(6)
    r = p.add_run(text)
    r.font.name = 'Times New Roman'
    r.font.size = Pt(13)
    r.font.bold = True
    return p

def add_h2(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(4)
    r = p.add_run(text)
    r.font.name = 'Times New Roman'
    r.font.size = Pt(11.5)
    r.font.bold = True
    return p

def add_body(text, space_after=6):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.25
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
    "Dalam rekayasa perangkat lunak enterprise modern, arsitektur monolitik konvensional kerap kali menghadapi "
    "kendala degradasi keterawatan (maintainability) dan tingginya tingkat ketergantungan antar komponen (high coupling) "
    "seiring bertambahnya kompleksitas fitur sistem. Pendekatan Modular Monolith yang dipadukan dengan prinsip "
    "Domain-Driven Design (DDD) hadir sebagai solusi arsitektural yang tangguh: mempertahankan kepraktisan "
    "operasional dan deployment tunggal aplikasi monolitik, sembari memberlakukan batas domain (Bounded Context) yang tegas "
    "dan disiplin sebagaimana arsitektur microservices."
)
add_body(
    "Pada praktikum Pertemuan ke-6 mata kuliah Backend Development (DT199), mahasiswa mempelajari teknik-teknik pengelolaan data "
    "tingkat lanjut menggunakan framework Laravel 13. Materi pokok yang dipelajari mencakup perancangan relasi Eloquent lanjutan "
    "(Many-to-Many dengan kolom pivot custom added_at, relasi Self-referencing hierarkis, relasi agregat HasMany), "
    "eliminasi masalah performa N+1 Query melalui strategi Eager Loading, penjaminan konsistensi data atomik menggunakan "
    "Database Transaction dengan auto-rollback, penerapan Soft Deletes untuk jejak audit (audit trail), "
    "perancangan Value Objects yang immutable, serta komunikasi nir-kopling melalui Domain Events."
)

add_h2("1.2 Maksud dan Tujuan Praktikum")
add_body("Praktikum ini bertujuan agar mahasiswa mampu:")
add_body("1. Menjelaskan dan mengimplementasikan konsep Domain-Driven Design (DDD) dan Bounded Context dalam arsitektur Modular Monolith pada framework Laravel 13.")
add_body("2. Mengimplementasikan berbagai relasi Eloquent lanjutan: Many-to-Many dengan kolom pivot added_at, Self-referencing (Category induk ke sub-kategori), dan relasi agregat HasMany.")
add_body("3. Menganalisis serta mengeliminasi masalah N+1 Query menggunakan Eager Loading (with(...)) dan menyusun Query Scopes yang reusable.")
add_body("4. Menerapkan Database Transaction (DB::transaction) untuk menjamin atomisitas transaksi sirkulasi buku, serta membuktikan mekanisme rollback otomatis saat terjadi kegagalan invariant bisnis.")
add_body("5. Mengimplementasikan Soft Deletes dan fungsi restore data terhapus untuk menjamin integritas riwayat data historis.")
add_body("6. Membangun Value Object (ISBN dan Denda) yang memvalidasi format data dan menghitung denda keterlambatan secara otomatis.")
add_body("7. Menerapkan Domain Event (BookBorrowed) dan Listener guna menjaga integritas batas antar konteks tanpa ketergantungan langsung.")

add_h2("1.3 Ruang Lingkup Sistem Perpustakaan Modular")
add_body(
    "Studi kasus yang dikerjakan adalah Sistem Informasi Perpustakaan Modular yang terbagi secara independen menjadi "
    "tiga Bounded Context utama dan satu Shared Kernel:\n"
    "a. Catalog Context: Mengelola data master buku, pengarang, penerbit, serta hierarki kategori buku berjenjang.\n"
    "b. Membership Context: Mengelola data master anggota perpustakaan, hak akses (roles), serta status keanggotaan.\n"
    "c. Circulation Context: Memproses transaksi peminjaman buku atomik, snapshot data historis, pencatatan keterlambatan, pengembalian, dan penghitungan denda.\n"
    "d. Shared Kernel: Berisi kontrak antarmuka (interfaces/contracts), Value Objects umum, dan custom domain exceptions yang dibagi pakai antar modul secara terkontrol."
)

doc.add_page_break()

# ==============================================================================
# BAB II: PERANCANGAN SISTEM
# ==============================================================================
add_h1("BAB II: PERANCANGAN SISTEM")

add_h2("2.1 Diagram Bounded Context dan Shared Kernel")
add_body(
    "Prinsip utama Domain-Driven Design menegaskan bahwa setiap Bounded Context memiliki model domain dan kepemilikan data "
    "(data ownership) sendiri. Modul Sirkulasi tidak diperkenankan mengakses tabel database atau model Eloquent milik modul "
    "Katalog secara langsung. Seluruh interaksi lintas modul harus melalui kontrak abstraksi (Interface) yang ditempatkan pada "
    "Shared Kernel atau dipicu melalui Domain Event. Gambar 2.1 menyajikan diagram Bounded Context sistem perpustakaan modular:"
)

# Image 1
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
img1 = r"d:\project6\laporan\images\diagram_bounded_context_bw.png"
if os.path.exists(img1):
    p.add_run().add_picture(img1, width=Inches(5.8))
p_cap = doc.add_paragraph()
p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p_cap.add_run("Gambar 2.1 Diagram Bounded Context dan Shared Kernel (Format Monochrome)")
r.font.size = Pt(9.5)
r.font.italic = True

add_h2("2.2 Analisis Aggregate Root dan Invariant Bisnis")
add_body(
    "Aggregate adalah sekumpulan objek domain (Entities dan Value Objects) yang diperlakukan sebagai satu kesatuan unit operasional. "
    "Pintu masuk utama aggregate dikontrol oleh Aggregate Root, yang bertanggung jawab mutlak memastikan terpeliharanya invariant (aturan validasi bisnis)."
)

tbl_agg = doc.add_table(rows=4, cols=4)
tbl_agg.alignment = WD_TABLE_ALIGNMENT.CENTER
headers_agg = ["Bounded Context", "Aggregate Root", "Entities di Dalamnya", "Invariant (Aturan Bisnis Utama)"]
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
    ("Catalog Context", "Book (Buku)", "Category, Author, Publisher", "Stok buku tidak boleh bernilai negatif; ISBN harus valid 10 atau 13 digit; Hanya buku berstatus aktif yang dapat dipinjam."),
    ("Membership Context", "Member (Anggota)", "Role", "Email dan kode anggota harus unik; Peminjaman hanya diizinkan untuk anggota dengan status 'active'."),
    ("Circulation Context", "Loan (Peminjaman)", "LoanDetail, Fine (Denda)", "Peminjaman wajib memotong stok buku; Detail pinjaman wajib menyimpan snapshot data buku; Denda dihitung otomatis Rp 2.000/hari.")
]

for row_idx, data in enumerate(agg_data, start=1):
    for col_idx, val in enumerate(data):
        cell = tbl_agg.cell(row_idx, col_idx)
        set_cell_background(cell, "FFFFFF" if row_idx % 2 != 0 else "F9F9F9")
        set_cell_margins(cell, top=100, bottom=100, left=150, right=150)
        p = cell.paragraphs[0]
        r = p.add_run(val)
        r.font.size = Pt(9)

doc.add_paragraph().paragraph_format.space_after = Pt(8)

add_h2("2.3 Entity Relationship Diagram (ERD) dan Snapshot Pattern")
add_body(
    "Desain relasi database pada aplikasi ini mengimplementasikan spesifikasi teknis berikut:\n"
    "1. Relasi Many-to-Many dengan Pivot: Relasi antara buku dan kategori melalui tabel pivot 'book_category' yang memuat timestamp 'added_at'.\n"
    "2. Relasi Self-Referencing: Tabel 'categories' memiliki foreign key 'parent_id' yang merujuk pada tabel itu sendiri untuk mendukung sub-kategori berjenjang.\n"
    "3. Relasi Agregat HasMany: Relasi 'loans' ke 'loan_details' bersifat One-to-Many dalam batas agregat peminjaman.\n"
    "4. Snapshot Pattern (Data Historis): Tabel 'loan_details' menduplikasi kolom 'book_title' dan 'book_isbn' saat transaksi peminjaman dibuat. Pola ini menjamin bahwa perubahan judul atau perbaikan data master buku di kemudian hari tidak akan merusak keaslian bukti riwayat transaksi peminjaman masa lalu."
)

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
img2 = r"d:\project6\laporan\images\diagram_erd_bw.png"
if os.path.exists(img2):
    p.add_run().add_picture(img2, width=Inches(5.8))
p_cap = doc.add_paragraph()
p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p_cap.add_run("Gambar 2.2 Entity Relationship Diagram (ERD) Sistem Perpustakaan (Format Monochrome)")
r.font.size = Pt(9.5)
r.font.italic = True

add_h2("2.4 Diagram Alur Database Transaction dan Mekanisme Auto-Rollback")
add_body(
    "Operasi peminjaman buku menuntut pemenuhan karakteristik ACID (Atomicity, Consistency, Isolation, Durability). "
    "Operasi pembuatan peminjaman dibungkus dalam blok DB::transaction(). Ketika salah satu buku memiliki stok kosong, "
    "sistem segera melempar InsufficientStockException, yang memicu pembatalan total (auto-rollback) terhadap seluruh instruksi SQL dalam transaksi tersebut."
)

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
img3 = r"d:\project6\laporan\images\diagram_transaction_flow_bw.png"
if os.path.exists(img3):
    p.add_run().add_picture(img3, width=Inches(4.6))
p_cap = doc.add_paragraph()
p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p_cap.add_run("Gambar 2.3 Flowchart Database Transaction dan Mekanisme Rollback (Format Monochrome)")
r.font.size = Pt(9.5)
r.font.italic = True

doc.add_page_break()

# ==============================================================================
# BAB III: IMPLEMENTASI SISTEM
# ==============================================================================
add_h1("BAB III: IMPLEMENTASI SISTEM")

add_h2("3.1 Struktur Direktori Bounded Context (Modular Monolith)")
add_body(
    "Aplikasi disusun dengan memisahkan domain ke dalam direktori app/Modules/ yang terdaftar pada PSR-4 autoloading composer.json:"
)
code_dir = (
    "app/Modules/\n"
    "├── Catalog/\n"
    "│   ├── Migrations/ (create_categories_table, create_books_table, create_book_category_table)\n"
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

add_h2("3.2 Implementasi Shared Kernel (Value Objects, Exceptions, Contracts)")
add_body(
    "Value Object 'ISBN' memastikan bahwa nomor identitas buku divalidasi checksum digitnya (ISBN-10 atau ISBN-13):"
)
code_isbn = (
    "namespace Modules\\Shared\\ValueObjects;\n"
    "use InvalidArgumentException;\n\n"
    "class ISBN {\n"
    "    private string $value;\n"
    "    public function __construct(string $value) {\n"
    "        $cleaned = preg_replace('/[^0-9X]/i', '', $value);\n"
    "        if (!$this->isValid($cleaned)) throw new InvalidArgumentException(\"Format ISBN tidak valid: {$value}\");\n"
    "        $this->value = strtoupper(trim($value));\n"
    "    }\n"
    "    // method validateIsbn10() & validateIsbn13()\n"
    "}"
)
add_code_block(doc, code_isbn)

add_body(
    "Value Object 'Denda' mengkapsulasi logika tarif harian dan penghitungan denda keterlambatan secara otomatis:"
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
    "    public function formatRupiah(): string { return 'Rp ' . number_format($this->amount, 0, ',', '.'); }\n"
    "}"
)
add_code_block(doc, code_denda)

add_h2("3.3 Implementasi Catalog Context (Buku, Kategori Hierarkis, Pivot added_at)")
add_body(
    "Model 'Category' mendukung struktur kategori hierarkis (Self-referencing) dan relasi Many-to-Many dengan pivot 'added_at':"
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
    "    public function books() { return $this->belongsToMany(Book::class, 'book_category')->withPivot('added_at'); }\n"
    "}"
)
add_code_block(doc, code_cat)

add_body(
    "Model 'Book' dilengkapi Soft Deletes dan Query Scopes reusable:"
)
code_book = (
    "namespace Modules\\Catalog\\Models;\n"
    "use Illuminate\\Database\\Eloquent\\Model;\n"
    "use Illuminate\\Database\\Eloquent\\SoftDeletes;\n"
    "use Illuminate\\Database\\Eloquent\\Builder;\n\n"
    "class Book extends Model {\n"
    "    use SoftDeletes;\n"
    "    public function scopeAvailable(Builder $query): Builder { return $query->where('is_active', true)->where('stock', '>', 0); }\n"
    "    public function scopeSearch(Builder $query, string $k): Builder {\n"
    "        return $query->where(fn($q) => $q->where('title', 'like', \"%$k%\")->orWhere('author', 'like', \"%$k%\")->orWhere('isbn', 'like', \"%$k%\"));\n"
    "    }\n"
    "    public function scopeByCategory(Builder $query, int $catId): Builder {\n"
    "        return $query->whereHas('categories', fn($q) => $q->where('categories.id', $catId));\n"
    "    }\n"
    "}"
)
add_code_block(doc, code_book)

add_h2("3.4 Implementasi Membership Context (Anggota, Role, MemberService)")
add_body(
    "Model 'Member' mengelola data keanggotaan dan berelasi ke roles. Method canBorrow() memvalidasi apakah anggota berhak meminjam:"
)
code_mem = (
    "namespace Modules\\Membership\\Models;\n"
    "use Illuminate\\Database\\Eloquent\\Model;\n"
    "use Illuminate\\Database\\Eloquent\\SoftDeletes;\n\n"
    "class Member extends Model {\n"
    "    use SoftDeletes;\n"
    "    protected $fillable = ['member_code', 'name', 'email', 'phone', 'status', 'max_loans'];\n"
    "    public function roles() { return $this->belongsToMany(Role::class, 'member_role'); }\n"
    "    public function canBorrow(): bool { return $this->status === 'active'; }\n"
    "}"
)
add_code_block(doc, code_mem)

add_h2("3.5 Implementasi Circulation Context (Peminjaman, Detail Snapshot, Denda)")
add_body(
    "Model 'Loan' dan 'LoanDetail' mengimplementasikan Snapshot Pattern untuk menjaga integritas data historis:"
)
code_circ_mod = (
    "namespace Modules\\Circulation\\Models;\n"
    "use Illuminate\\Database\\Eloquent\\Model;\n\n"
    "class LoanDetail extends Model {\n"
    "    protected $fillable = ['loan_id', 'book_id', 'book_title', 'book_isbn', 'returned_at'];\n"
    "    public function loan() { return $this->belongsTo(Loan::class); }\n"
    "}"
)
add_code_block(doc, code_circ_mod)

add_h2("3.6 Implementasi CirculationService dengan Database Transaction Atomik")
add_body(
    "Metode borrowBooks() membungkus seluruh tahapan bisnis peminjaman ke dalam transaksi atomik dengan auto-rollback:"
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
    "                'book_isbn' => $book['isbn'],   // SNAPSHOT\n"
    "            ]);\n"
    "            $this->bookService->reduceStock($bookId, 1);\n"
    "        }\n"
    "        event(new BookBorrowed($loan->load('details')));\n"
    "        return $loan->load('details');\n"
    "    });\n"
    "}"
)
add_code_block(doc, code_tx)

add_h2("3.7 Konfigurasi Service Provider di bootstrap/providers.php")
add_body(
    "Seluruh modul didaftarkan pada konfigurasi kernel Laravel 13 di bootstrap/providers.php:"
)
code_prov = (
    "return [\n"
    "    App\\Providers\\AppServiceProvider::class,\n"
    "    Modules\\Auth\\Providers\\AuthServiceProvider::class,\n"
    "    Modules\\Products\\Providers\\ProductServiceProvider::class,\n"
    "    Modules\\Catalog\\Providers\\CatalogServiceProvider::class,\n"
    "    Modules\\Membership\\Providers\\MembershipServiceProvider::class,\n"
    "    Modules\\Circulation\\Providers\\CirculationServiceProvider::class,\n"
    "];"
)
add_code_block(doc, code_prov)

add_h2("3.8 Riwayat Commit Git (Conventional Commits)")
add_body("Seluruh tahapan implementasi dicatat menggunakan riwayat commit Git yang terstruktur dan teratur:")

tbl_git = doc.add_table(rows=9, cols=3)
tbl_git.alignment = WD_TABLE_ALIGNMENT.CENTER
headers_git = ["Commit Hash", "Tipe & Pesan Commit", "Keterangan Komponen Modul"]
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
    ("b9d5b44", "chore: initialize laravel 13 project for praktikum backend 6", "Inisialisasi repositori Git dan proteksi file AI di .gitignore."),
    ("466e7b2", "feat(shared): implement ISBN, Denda, exceptions, and contracts", "Pembangunan Value Objects, Exceptions, dan Contracts Interface."),
    ("d6054f3", "feat(catalog): implement books, hierarchical categories, and service", "Migrasi, Model Buku-Kategori (pivot added_at), dan CatalogService."),
    ("fa76089", "feat(membership): implement member models, roles, and service", "Migrasi, Model Anggota, Roles, dan MemberService."),
    ("7c8a5b4", "feat(circulation): implement borrow transactions and BookBorrowed event", "Migrasi Peminjaman, Snapshot Detail, Domain Event, dan Transaksi."),
    ("2c153af", "feat: register module service providers in bootstrap/providers.php", "Pendaftaran seluruh provider modul ke arsitektur Laravel 13."),
    ("58933bf", "feat(seeders): implement LibrarySeeder with books and members", "Seeding data uji realistis dengan ISBN-13 tervalidasi."),
    ("33a6185", "test: add automated feature tests and interactive library demo command", "Pembuatan feature test suite otomatis dan console command demo.")
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
# BAB IV: PENGUJIAN SISTEM
# ==============================================================================
add_h1("BAB IV: PENGUJIAN SISTEM")

add_h2("4.1 Pengujian Relasi Lanjutan (Self-Referencing & Many-to-Many Pivot)")
add_body(
    "Pengujian relasi lanjutan membuktikan bahwa relasi Self-referencing berhasil mengambil anak kategori dari induknya, "
    "dan relasi Many-to-Many berhasil membaca kolom pivot added_at:"
)
code_rel_out = (
    "1. PENGUJIAN RELASI LANJUTAN\n"
    " a) Self-referencing Category (Parent -> Children):\n"
    " - Induk: [Teknologi & Komputer] -> Sub-Kategori: [Pemrograman & Algoritma, Kecerdasan Buatan]\n"
    " - Induk: [Sains & Matematika] -> Sub-Kategori: [Fisika Terapan]\n\n"
    " b) Many-to-Many Pivot (Buku <-> Kategori dengan added_at):\n"
    " - Judul Buku: Clean Code: A Handbook of Agile Software Craftsmanship\n"
    " * Kategori: Teknologi & Komputer (Pivot added_at: 2026-11-08 13:59:22)\n"
    " * Kategori: Pemrograman & Algoritma (Pivot added_at: 2026-11-08 13:59:22)"
)
add_code_block(doc, code_rel_out)

add_h2("4.2 Pengujian Query Optimization (Eliminasi Masalah N+1 Query)")
add_body(
    "Pengujian dilakukan dengan mengaktifkan pencatatan log query SQL menggunakan DB::enableQueryLog(). "
    "Pada metode Lazy Loading biasa, perulangan 5 record peminjaman memicu 1 query induk ditambah 10 query anak (11 query SQL). "
    "Sebaliknya, dengan menerapkan strategi Eager Loading with(['details', 'member']), seluruh relasi dimuat hanya dalam 3 query konstan."
)

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
img4 = r"d:\project6\laporan\images\chart_query_comparison_bw.png"
if os.path.exists(img4):
    p.add_run().add_picture(img4, width=Inches(5.5))
p_cap = doc.add_paragraph()
p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p_cap.add_run("Gambar 4.1 Grafik Perbandingan Eksekusi Query Database (N+1 Query vs Eager Loading)")
r.font.size = Pt(9.5)
r.font.italic = True

tbl_n1 = doc.add_table(rows=3, cols=4)
tbl_n1.alignment = WD_TABLE_ALIGNMENT.CENTER
headers_n1 = ["Metode Pengambilan Data", "Jumlah Data Record", "Jumlah Query SQL", "Efisiensi Performa"]
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
    ("Tanpa Eager Loading (Lazy Loading loop)", "5 Data Peminjaman", "11 Query SQL", "BOROS & LAMBAT (N+1 Query Problem)"),
    ("Dengan Eager Loading with(['details', 'member'])", "5 Data Peminjaman", "3 Query SQL", "SANGAT EFISIEN & CEPAT (Teroptimasi)")
]
for row_idx, data in enumerate(n1_data, start=1):
    for col_idx, val in enumerate(data):
        cell = tbl_n1.cell(row_idx, col_idx)
        set_cell_margins(cell, top=80, bottom=80, left=150, right=150)
        p = cell.paragraphs[0]
        r = p.add_run(val)
        r.font.size = Pt(8.5)

doc.add_paragraph().paragraph_format.space_after = Pt(8)

add_h2("4.3 Pengujian Query Scopes (Available, Search, ByCategory)")
add_body(
    "Query Scopes pada model Book berhasil memfilter data secara dinamis:\n"
    "- Book::available(): Hanya memunculkan buku dengan is_active = true dan stock > 0.\n"
    "- Book::search('Clean Code'): Mengembalikan buku dengan judul atau pengarang terkait.\n"
    "- Book::byCategory($categoryId): Mengembalikan daftar buku pada kategori tertentu melalui relasi whereHas."
)

add_h2("4.4 Pengujian Database Transaction Berhasil (Atomisitas Pemotongan Stok)")
add_body(
    "Saat peminjaman buku dengan stok mencukupi dilakukan, sistem memotong stok buku sebanyak 1, membuat record pada tabel loans, "
    "mencatat snapshot pada loan_details, dan memancarkan event BookBorrowed dalam satu kesatuan unit atomik."
)

add_h2("4.5 Pengujian Database Transaction Rollback (Stok Kosong)")
add_body(
    "Pengujian dilakukan dengan mensimulasikan peminjaman buku yang stoknya kosong ('The Pragmatic Programmer', stok: 0). "
    "Sistem mendeteksi kekurangan stok saat transaksi berjalan dan melempar InsufficientStockException. "
    "Hasil pengujian membuktikan bahwa DB::transaction() membatalkan seluruh operasi secara utuh:"
)
code_rb_out = (
    "Mencoba meminjam buku dengan stok kosong ('The Pragmatic Programmer: Your Journey To Mastery', stok: 0)...\n"
    "[BERHASIL] Exception tertangkap: Stok buku 'The Pragmatic Programmer' tidak mencukupi. Tersedia: 0, diminta: 1.\n"
    "[VERIFIKASI ROLLBACK] Record Loan sebelum: 5, sesudah: 5\n"
    "-> DB::transaction() berhasil membatalkan seluruh operasi secara atomik! Konsistensi basis data terjaga 100%."
)
add_code_block(doc, code_rb_out)

add_h2("4.6 Pengujian Soft Deletes dan Restore Data Terhapus")
add_body(
    "Pengujian membuktikan bahwa penghapusan data dengan delete() tidak menghilangkan baris data secara permanen, melainkan mengisi kolom deleted_at. "
    "Data yang terhapus dapat dipulihkan secara instan menggunakan restore():"
)
code_sd_out = (
    "Menghapus buku #1 ('Clean Code') secara Soft Delete...\n"
    "- Book::count() (Record Aktif)               : 4 Buku\n"
    "- Book::withTrashed()->count() (Total Fisik)  : 5 Buku\n"
    "Mengembalikan buku dengan restore()...\n"
    "- Book::count() setelah restore             : 5 Buku [DATA PULIH SEMPURNA]"
)
add_code_block(doc, code_sd_out)

add_h2("4.7 Pengujian Value Objects (ISBN & Kalkulasi Denda)")
add_body(
    "Pengujian memverifikasi bahwa ISBN memvalidasi checksum digit 10 dan 13 secara ketat serta melempar InvalidArgumentException jika format salah. "
    "Value Object Denda secara otomatis menghitung tarif: 5 Hari keterlambatan x Rp 2.000 menghasilkan 'Rp 10.000'."
)

add_h2("4.8 Pengujian Domain Event BookBorrowed & Listener Logging")
add_body(
    "Domain Event BookBorrowed terbukti dipancarkan sesaat setelah transaksi commit. "
    "Listener LogBookBorrowedActivity berhasil mencatat aktivitas peminjaman ke dalam storage/logs/laravel.log tanpa mengganggu eksekusi utama."
)

add_h2("4.9 Matriks Hasil Pengujian Otomatis (Automated Testing Pest / PHPUnit)")
add_body(
    "Seluruh aspek fungsional sistem diuji menggunakan automated test suite pada tests/Feature/LibraryModularDDDTest.php. "
    "Seluruh 6 unit skenario dinyatakan lulus 100%:"
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
    "Berdasarkan seluruh tahapan perancangan, implementasi, dan pengujian yang telah diselesaikan pada Sistem Perpustakaan Modular berbasis Laravel 13, dapat ditarik beberapa kesimpulan pokok:\n\n"
    "1. Modularitas & Decoupling: Penerapan Modular Monolith dengan Domain-Driven Design (DDD) berhasil memecah kerumitan logika sistem ke dalam Bounded Context yang jelas (Catalog, Membership, Circulation, Shared Kernel). Ketergantungan langsung antar tabel berhasil dihilangkan melalui perantara Contract (Interface) dan Domain Event.\n\n"
    "2. Fleksibilitas Relasi Eloquent: Relasi Many-to-Many dengan pivot custom (added_at) dan Self-referencing hierarkis terbukti sangat ampuh memodelkan hubungan entitas dunia nyata, sedangkan Snapshot Pattern pada detail transaksi menjamin keaslian data historis.\n\n"
    "3. Efisiensi Query yang Terukur: Penggunaan Eager Loading terbukti memangkas jumlah eksekusi query dari 11 query menjadi 3 query konstan, mengeliminasi risiko kelambatan sistem akibat masalah N+1 Query.\n\n"
    "4. Konsistensi Data Transaksional: Pemanfaatan Database Transaction (DB::transaction) menjamin integritas data secara atomik, di mana kegagalan bisnis pada satu komponen secara otomatis membatalkan seluruh operasi tanpa anomali data.\n\n"
    "5. Integritas Domain melalui Value Objects: Pemakaian Value Object (ISBN dan Denda) memperkuat domain model aplikasi dengan memastikan data selalu valid sejak awal pembuatan objek."
)

# ==============================================================================
# LAMPIRAN
# ==============================================================================
add_h1("LAMPIRAN: TAUTAN REPOSITORY GITHUB")
add_body("Seluruh kode sumber, riwayat commit Git, modul, dan script pengujian dapat diakses pada repositori publik berikut:")
p_link = doc.add_paragraph()
r_link = p_link.add_run("🔗 https://github.com/panjiprasetyaa/praktikum-backend-6.git")
r_link.font.name = 'Consolas'
r_link.font.size = Pt(11)
r_link.font.bold = True

docx_path = r"d:\project6\laporan\LAPORAN_PRAKTIKUM_PERTEMUAN_6.docx"
doc.save(docx_path)
print("Word (.docx) successfully created:", docx_path)

# ==============================================================================
# BUILD HTML & PDF
# ==============================================================================
html_content = """<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<title>Laporan Praktikum Backend Development - Pertemuan 6</title>
<style>
  @page {
    size: A4;
    margin: 2.5cm 2.5cm 2.5cm 2.5cm;
    @bottom-right {
      content: counter(page);
    }
  }
  body {
    font-family: 'Times New Roman', Times, serif;
    font-size: 11.5pt;
    line-height: 1.35;
    color: #000;
    margin: 0;
    padding: 0;
  }
  .page-break {
    page-break-before: always;
  }
  .cover {
    text-align: center;
    padding-top: 15px;
    height: 90vh;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }
  .cover-header {
    font-size: 14pt;
    font-weight: bold;
    line-height: 1.3;
  }
  .cover-logo {
    margin: 50px auto;
  }
  .cover-logo img {
    width: 170px;
    height: 170px;
  }
  .cover-meta {
    font-size: 11pt;
    line-height: 1.6;
    margin-bottom: 20px;
  }
  .cover-meta .dosen {
    margin-bottom: 35px;
  }
  .cover-meta .mahasiswa {
    font-weight: bold;
    font-size: 11.5pt;
  }
  h1 {
    font-size: 13.5pt;
    font-weight: bold;
    margin-top: 24px;
    margin-bottom: 12px;
    border-bottom: 1.5px solid #000;
    padding-bottom: 4px;
    text-transform: uppercase;
  }
  h2 {
    font-size: 11.5pt;
    font-weight: bold;
    margin-top: 16px;
    margin-bottom: 8px;
  }
  p {
    text-align: justify;
    margin-top: 0;
    margin-bottom: 10px;
  }
  table {
    width: 100%;
    border-collapse: collapse;
    margin: 14px 0;
    font-size: 9.5pt;
  }
  table, th, td {
    border: 1px solid #000;
  }
  th {
    background-color: #f0f0f0;
    font-weight: bold;
    text-align: center;
    padding: 8px;
  }
  td {
    padding: 6px 8px;
    vertical-align: top;
  }
  .code-block {
    background-color: #f8f8f8;
    border: 1px solid #ccc;
    border-left: 3px solid #333;
    padding: 10px 12px;
    font-family: 'Consolas', 'Courier New', monospace;
    font-size: 8.5pt;
    white-space: pre-wrap;
    word-break: break-all;
    margin: 12px 0;
    line-height: 1.25;
  }
  .image-container {
    text-align: center;
    margin: 16px 0;
  }
  .image-container img {
    max-width: 88%;
    height: auto;
    border: 1px solid #ddd;
  }
  .caption {
    font-size: 9.5pt;
    font-style: italic;
    margin-top: 6px;
    text-align: center;
  }
  ol, ul {
    margin-top: 0;
    margin-bottom: 10px;
    padding-left: 24px;
  }
  li {
    margin-bottom: 4px;
    text-align: justify;
  }
  /* TOC Table styling */
  .toc-table {
    width: 100%;
    border: none;
    margin-top: 15px;
  }
  .toc-table td {
    border: none;
    padding: 3px 0;
    font-size: 10.5pt;
  }
  .toc-leader {
    border-bottom: 1px dotted #000;
    height: 14px;
  }
  .toc-bold {
    font-weight: bold;
  }
</style>
</head>
<body>

<!-- COVER -->
<div class="cover">
  <div class="cover-header">
    LAPORAN PRAKTIKUM<br>
    BACKEND DEVELOPMENT<br>
    PENGELOLAAN DATA LANJUTAN<br>
    MODULAR MONOLITH & DOMAIN-DRIVEN DESIGN (DDD)
  </div>

  <div class="cover-logo">
    <img src="images/logo_amikom.png" alt="Logo Amikom">
  </div>

  <div class="cover-meta">
    <div class="dosen">
      Dosen Pengampu:<br>
      <strong>Hastari Utama, S.Kom., M.Cs.</strong>
    </div>

    <div>Disusun Oleh:</div>
    <div class="mahasiswa">
      Nama Mahasiswa : Muhammad Imam Panji Prasetya<br>
      NIM : 25.01.5303<br>
      Kelas : D3 Teknik Informatika
    </div>
  </div>
</div>

<div class="page-break"></div>

<!-- DAFTAR ISI -->
<h1 style="text-align: center; border-bottom: none; margin-bottom: 25px;">DAFTAR ISI</h1>

<table class="toc-table">
  <tr class="toc-bold">
    <td>BAB I: PENDAHULUAN</td>
    <td style="width: 60%;"><div class="toc-leader"></div></td>
    <td style="text-align: right; width: 40px;">1</td>
  </tr>
  <tr>
    <td style="padding-left: 15px;">1.1 Latar Belakang</td>
    <td><div class="toc-leader"></div></td>
    <td style="text-align: right;">1</td>
  </tr>
  <tr>
    <td style="padding-left: 15px;">1.2 Maksud dan Tujuan Praktikum</td>
    <td><div class="toc-leader"></div></td>
    <td style="text-align: right;">1</td>
  </tr>
  <tr>
    <td style="padding-left: 15px;">1.3 Ruang Lingkup Sistem Perpustakaan Modular</td>
    <td><div class="toc-leader"></div></td>
    <td style="text-align: right;">2</td>
  </tr>
  <tr class="toc-bold">
    <td>BAB II: PERANCANGAN SISTEM</td>
    <td><div class="toc-leader"></div></td>
    <td style="text-align: right;">3</td>
  </tr>
  <tr>
    <td style="padding-left: 15px;">2.1 Diagram Bounded Context dan Shared Kernel</td>
    <td><div class="toc-leader"></div></td>
    <td style="text-align: right;">3</td>
  </tr>
  <tr>
    <td style="padding-left: 15px;">2.2 Analisis Aggregate Root dan Invariant Bisnis</td>
    <td><div class="toc-leader"></div></td>
    <td style="text-align: right;">4</td>
  </tr>
  <tr>
    <td style="padding-left: 15px;">2.3 Entity Relationship Diagram (ERD) dan Snapshot Pattern</td>
    <td><div class="toc-leader"></div></td>
    <td style="text-align: right;">5</td>
  </tr>
  <tr>
    <td style="padding-left: 15px;">2.4 Diagram Alur Database Transaction dan Mekanisme Auto-Rollback</td>
    <td><div class="toc-leader"></div></td>
    <td style="text-align: right;">6</td>
  </tr>
  <tr class="toc-bold">
    <td>BAB III: IMPLEMENTASI SISTEM</td>
    <td><div class="toc-leader"></div></td>
    <td style="text-align: right;">7</td>
  </tr>
  <tr>
    <td style="padding-left: 15px;">3.1 Struktur Direktori Bounded Context (Modular Monolith)</td>
    <td><div class="toc-leader"></div></td>
    <td style="text-align: right;">7</td>
  </tr>
  <tr>
    <td style="padding-left: 15px;">3.2 Implementasi Shared Kernel (Value Objects, Exceptions, Contracts)</td>
    <td><div class="toc-leader"></div></td>
    <td style="text-align: right;">8</td>
  </tr>
  <tr>
    <td style="padding-left: 15px;">3.3 Implementasi Catalog Context (Buku, Kategori Hierarkis, Pivot added_at)</td>
    <td><div class="toc-leader"></div></td>
    <td style="text-align: right;">9</td>
  </tr>
  <tr>
    <td style="padding-left: 15px;">3.4 Implementasi Membership Context (Anggota, Role, MemberService)</td>
    <td><div class="toc-leader"></div></td>
    <td style="text-align: right;">10</td>
  </tr>
  <tr>
    <td style="padding-left: 15px;">3.5 Implementasi Circulation Context (Peminjaman, Detail Snapshot, Denda)</td>
    <td><div class="toc-leader"></div></td>
    <td style="text-align: right;">11</td>
  </tr>
  <tr>
    <td style="padding-left: 15px;">3.6 Implementasi CirculationService dengan Database Transaction Atomik</td>
    <td><div class="toc-leader"></div></td>
    <td style="text-align: right;">12</td>
  </tr>
  <tr>
    <td style="padding-left: 15px;">3.7 Konfigurasi Service Provider di bootstrap/providers.php</td>
    <td><div class="toc-leader"></div></td>
    <td style="text-align: right;">13</td>
  </tr>
  <tr>
    <td style="padding-left: 15px;">3.8 Riwayat Commit Git (Conventional Commits)</td>
    <td><div class="toc-leader"></div></td>
    <td style="text-align: right;">13</td>
  </tr>
  <tr class="toc-bold">
    <td>BAB IV: PENGUJIAN SISTEM</td>
    <td><div class="toc-leader"></div></td>
    <td style="text-align: right;">14</td>
  </tr>
  <tr>
    <td style="padding-left: 15px;">4.1 Pengujian Relasi Lanjutan (Self-Referencing & Many-to-Many Pivot)</td>
    <td><div class="toc-leader"></div></td>
    <td style="text-align: right;">14</td>
  </tr>
  <tr>
    <td style="padding-left: 15px;">4.2 Pengujian Query Optimization (Eliminasi Masalah N+1 Query)</td>
    <td><div class="toc-leader"></div></td>
    <td style="text-align: right;">15</td>
  </tr>
  <tr>
    <td style="padding-left: 15px;">4.3 Pengujian Query Scopes (Available, Search, ByCategory)</td>
    <td><div class="toc-leader"></div></td>
    <td style="text-align: right;">16</td>
  </tr>
  <tr>
    <td style="padding-left: 15px;">4.4 Pengujian Database Transaction Berhasil (Atomisitas Pemotongan Stok)</td>
    <td><div class="toc-leader"></div></td>
    <td style="text-align: right;">17</td>
  </tr>
  <tr>
    <td style="padding-left: 15px;">4.5 Pengujian Database Transaction Rollback (Stok Kosong)</td>
    <td><div class="toc-leader"></div></td>
    <td style="text-align: right;">18</td>
  </tr>
  <tr>
    <td style="padding-left: 15px;">4.6 Pengujian Soft Deletes dan Restore Data Terhapus</td>
    <td><div class="toc-leader"></div></td>
    <td style="text-align: right;">19</td>
  </tr>
  <tr>
    <td style="padding-left: 15px;">4.7 Pengujian Value Objects (ISBN & Kalkulasi Denda)</td>
    <td><div class="toc-leader"></div></td>
    <td style="text-align: right;">20</td>
  </tr>
  <tr>
    <td style="padding-left: 15px;">4.8 Pengujian Domain Event BookBorrowed & Listener Logging</td>
    <td><div class="toc-leader"></div></td>
    <td style="text-align: right;">21</td>
  </tr>
  <tr>
    <td style="padding-left: 15px;">4.9 Matriks Hasil Pengujian Otomatis (Automated Testing Pest / PHPUnit)</td>
    <td><div class="toc-leader"></div></td>
    <td style="text-align: right;">22</td>
  </tr>
  <tr class="toc-bold">
    <td>BAB V: KESIMPULAN</td>
    <td><div class="toc-leader"></div></td>
    <td style="text-align: right;">23</td>
  </tr>
  <tr class="toc-bold">
    <td>LAMPIRAN</td>
    <td><div class="toc-leader"></div></td>
    <td style="text-align: right;">24</td>
  </tr>
</table>

<div class="page-break"></div>

<!-- BAB I -->
<h1>BAB I: PENDAHULUAN</h1>
<h2>1.1 Latar Belakang</h2>
<p>
Dalam rekayasa perangkat lunak enterprise modern, arsitektur monolitik konvensional kerap kali menghadapi kendala degradasi keterawatan (maintainability) dan tingginya tingkat ketergantungan antar komponen (high coupling) seiring bertambahnya kompleksitas fitur sistem. Pendekatan Modular Monolith yang dipadukan dengan prinsip Domain-Driven Design (DDD) hadir sebagai solusi arsitektural yang tangguh: mempertahankan kepraktisan operasional dan deployment tunggal aplikasi monolitik, sembari memberlakukan batas domain (Bounded Context) yang tegas dan disiplin sebagaimana arsitektur microservices.
</p>
<p>
Pada praktikum Pertemuan ke-6 mata kuliah Backend Development (DT199), mahasiswa mempelajari teknik-teknik pengelolaan data tingkat lanjut menggunakan framework Laravel 13. Materi pokok yang dipelajari mencakup perancangan relasi Eloquent lanjutan (Many-to-Many dengan kolom pivot custom added_at, relasi Self-referencing hierarkis, relasi agregat HasMany), eliminasi masalah performa N+1 Query melalui strategi Eager Loading, penjaminan konsistensi data atomik menggunakan Database Transaction dengan auto-rollback, penerapan Soft Deletes untuk jejak audit (audit trail), perancangan Value Objects yang immutable, serta komunikasi nir-kopling melalui Domain Events.
</p>

<h2>1.2 Maksud dan Tujuan Praktikum</h2>
<p>Praktikum ini bertujuan agar mahasiswa mampu:</p>
<ol>
  <li>Menjelaskan dan mengimplementasikan konsep Domain-Driven Design (DDD) dan Bounded Context dalam arsitektur Modular Monolith pada framework Laravel 13.</li>
  <li>Mengimplementasikan berbagai relasi Eloquent lanjutan: Many-to-Many dengan kolom pivot added_at, Self-referencing (Category induk ke sub-kategori), dan relasi agregat HasMany.</li>
  <li>Menganalisis serta mengeliminasi masalah N+1 Query menggunakan Eager Loading (with(...)) dan menyusun Query Scopes yang reusable.</li>
  <li>Menerapkan Database Transaction (DB::transaction) untuk menjamin atomisitas transaksi sirkulasi buku, serta membuktikan mekanisme rollback otomatis saat terjadi kegagalan invariant bisnis.</li>
  <li>Mengimplementasikan Soft Deletes dan fungsi restore data terhapus untuk menjamin integritas riwayat data historis.</li>
  <li>Membangun Value Object (ISBN dan Denda) yang memvalidasi format data dan menghitung denda keterlambatan secara otomatis.</li>
  <li>Menerapkan Domain Event (BookBorrowed) dan Listener guna menjaga integritas batas antar konteks tanpa ketergantungan langsung.</li>
</ol>

<h2>1.3 Ruang Lingkup Sistem Perpustakaan Modular</h2>
<p>
Studi kasus yang dikerjakan adalah Sistem Informasi Perpustakaan Modular yang terbagi secara independen menjadi tiga Bounded Context utama dan satu Shared Kernel:
</p>
<ul>
  <li><strong>Catalog Context:</strong> Mengelola data master buku, pengarang, penerbit, serta hierarki kategori buku berjenjang.</li>
  <li><strong>Membership Context:</strong> Mengelola data master anggota perpustakaan, hak akses (roles), serta status keanggotaan.</li>
  <li><strong>Circulation Context:</strong> Memproses transaksi peminjaman buku atomik, snapshot data historis, pencatatan keterlambatan, pengembalian, dan penghitungan denda.</li>
  <li><strong>Shared Kernel:</strong> Berisi kontrak antarmuka (interfaces/contracts), Value Objects umum, dan custom domain exceptions yang dibagi pakai antar modul secara terkontrol.</li>
</ul>

<div class="page-break"></div>

<!-- BAB II -->
<h1>BAB II: PERANCANGAN SISTEM</h1>
<h2>2.1 Diagram Bounded Context dan Shared Kernel</h2>
<p>
Prinsip utama Domain-Driven Design menegaskan bahwa setiap Bounded Context memiliki model domain dan kepemilikan data (data ownership) sendiri. Modul Sirkulasi tidak diperkenankan mengakses tabel database atau model Eloquent milik modul Katalog secara langsung. Seluruh interaksi lintas modul harus melalui kontrak abstraksi (Interface) yang ditempatkan pada Shared Kernel atau dipicu melalui Domain Event.
</p>
<div class="image-container">
  <img src="images/diagram_bounded_context_bw.png" alt="Bounded Context">
  <div class="caption">Gambar 2.1 Diagram Bounded Context dan Shared Kernel (Format Monochrome)</div>
</div>

<h2>2.2 Analisis Aggregate Root dan Invariant Bisnis</h2>
<p>
Aggregate adalah sekumpulan objek domain (Entities dan Value Objects) yang diperlakukan sebagai satu kesatuan unit operasional. Pintu masuk utama aggregate dikontrol oleh Aggregate Root, yang bertanggung jawab mutlak memastikan terpeliharanya invariant (aturan validasi bisnis).
</p>

<table>
  <thead>
    <tr>
      <th style="width: 20%;">Bounded Context</th>
      <th style="width: 18%;">Aggregate Root</th>
      <th style="width: 25%;">Entities di Dalamnya</th>
      <th>Invariant (Aturan Bisnis Utama)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Catalog Context</strong></td>
      <td><code>Book (Buku)</code></td>
      <td>Category, Author, Publisher</td>
      <td>Stok buku tidak boleh bernilai negatif; ISBN harus valid 10 atau 13 digit; Hanya buku berstatus aktif yang dapat dipinjam.</td>
    </tr>
    <tr>
      <td><strong>Membership Context</strong></td>
      <td><code>Member (Anggota)</code></td>
      <td>Role</td>
      <td>Email dan kode anggota harus unik; Peminjaman hanya diizinkan untuk anggota dengan status 'active'.</td>
    </tr>
    <tr>
      <td><strong>Circulation Context</strong></td>
      <td><code>Loan (Peminjaman)</code></td>
      <td>LoanDetail, Fine (Denda)</td>
      <td>Peminjaman wajib memotong stok buku; Detail pinjaman wajib menyimpan snapshot data buku; Denda dihitung otomatis Rp 2.000/hari.</td>
    </tr>
  </tbody>
</table>

<h2>2.3 Entity Relationship Diagram (ERD) dan Snapshot Pattern</h2>
<p>
Perancangan relasi database mengimplementasikan relasi Many-to-Many pivot (book_category dengan added_at), Self-referencing (categories.parent_id), dan Snapshot Pattern pada loan_details (menyimpan salinan permanen book_title dan book_isbn saat pinjaman dibuat).
</p>
<div class="image-container">
  <img src="images/diagram_erd_bw.png" alt="ERD Diagram">
  <div class="caption">Gambar 2.2 Entity Relationship Diagram (ERD) Sistem Perpustakaan (Format Monochrome)</div>
</div>

<h2>2.4 Diagram Alur Database Transaction dan Mekanisme Auto-Rollback</h2>
<p>
Operasi peminjaman buku dibungkus dalam blok DB::transaction(). Ketika salah satu buku memiliki stok kosong, sistem segera melempar InsufficientStockException, yang memicu pembatalan total (auto-rollback) terhadap seluruh instruksi SQL dalam transaksi tersebut.
</p>
<div class="image-container">
  <img src="images/diagram_transaction_flow_bw.png" alt="Transaction Flow">
  <div class="caption">Gambar 2.3 Flowchart Database Transaction dan Mekanisme Rollback (Format Monochrome)</div>
</div>

<div class="page-break"></div>

<!-- BAB III -->
<h1>BAB III: IMPLEMENTASI SISTEM</h1>
<h2>3.1 Struktur Direktori Bounded Context (Modular Monolith)</h2>
<div class="code-block">app/Modules/
├── Catalog/ (Models, Migrations, Providers, Services)
├── Membership/ (Models, Migrations, Providers, Services)
├── Circulation/ (Models, Migrations, Providers, Services, Events, Listeners)
└── Shared/ (Contracts, Exceptions, ValueObjects)</div>

<h2>3.2 Implementasi Shared Kernel (Value Objects, Exceptions, Contracts)</h2>
<p>Value Object ISBN dan Denda menjamin validitas dan konsistensi data domain secara immutable:</p>
<div class="code-block">namespace Modules\Shared\ValueObjects;

class ISBN {
    private string $value;
    public function __construct(string $value) {
        $cleaned = preg_replace('/[^0-9X]/i', '', $value);
        if (!$this->isValid($cleaned)) throw new \InvalidArgumentException("Format ISBN tidak valid: {$value}");
        $this->value = strtoupper(trim($value));
    }
}</div>

<div class="code-block">namespace Modules\Shared\ValueObjects;

class Denda {
    private int $daysOverdue;
    private float $dailyRate;
    private float $amount;

    public function __construct(int $daysOverdue, float $dailyRate = 2000.0) {
        if ($daysOverdue < 0) throw new \InvalidArgumentException('Hari denda tidak boleh negatif');
        $this->daysOverdue = $daysOverdue;
        $this->dailyRate = $dailyRate;
        $this->amount = $daysOverdue * $dailyRate;
    }
    public function formatRupiah(): string { return 'Rp ' . number_format($this->amount, 0, ',', '.'); }
}</div>

<h2>3.3 Implementasi Catalog Context (Buku, Kategori Hierarkis, Pivot added_at)</h2>
<div class="code-block">class Category extends Model {
    use SoftDeletes;
    public function parent() { return $this->belongsTo(Category::class, 'parent_id'); }
    public function children() { return $this->hasMany(Category::class, 'parent_id'); }
    public function books() { return $this->belongsToMany(Book::class, 'book_category')->withPivot('added_at'); }
}</div>

<h2>3.4 Implementasi Membership Context (Anggota, Role, MemberService)</h2>
<div class="code-block">class Member extends Model {
    use SoftDeletes;
    public function roles() { return $this->belongsToMany(Role::class, 'member_role'); }
    public function canBorrow(): bool { return $this->status === 'active'; }
}</div>

<h2>3.5 Implementasi Circulation Context (Peminjaman, Detail Snapshot, Denda)</h2>
<div class="code-block">class LoanDetail extends Model {
    protected $fillable = ['loan_id', 'book_id', 'book_title', 'book_isbn', 'returned_at'];
    public function loan() { return $this->belongsTo(Loan::class); }
}</div>

<h2>3.6 Implementasi CirculationService dengan Database Transaction Atomik</h2>
<div class="code-block">public function borrowBooks(int $memberId, array $bookIds, int $loanDays = 7): Loan {
    return DB::transaction(function () use ($memberId, $bookIds, $loanDays) {
        if (!$this->memberService->canBorrow($memberId)) {
            throw new MemberNotEligibleException('Member tidak aktif / melampaui kuota.');
        }
        $loan = Loan::create([
            'loan_code' => 'LOAN-' . date('Ymd') . '-' . strtoupper(substr(uniqid(), -5)),
            'member_id' => $memberId,
            'borrowed_at' => now(),
            'due_date' => now()->addDays($loanDays),
            'status' => 'borrowed'
        ]);
        foreach ($bookIds as $bookId) {
            $book = $this->bookService->getBookForLoan($bookId);
            if (!$this->bookService->isStockAvailable($bookId, 1)) {
                throw new InsufficientStockException($book['title'], $book['stock'], 1);
            }
            LoanDetail::create([
                'loan_id' => $loan->id,
                'book_id' => $bookId,
                'book_title' => $book['title'],
                'book_isbn' => $book['isbn'],
            ]);
            $this->bookService->reduceStock($bookId, 1);
        }
        event(new BookBorrowed($loan->load('details')));
        return $loan->load('details');
    });
}</div>

<h2>3.7 Konfigurasi Service Provider di bootstrap/providers.php</h2>
<div class="code-block">return [
    App\Providers\AppServiceProvider::class,
    Modules\Auth\Providers\AuthServiceProvider::class,
    Modules\Products\Providers\ProductServiceProvider::class,
    Modules\Catalog\Providers\CatalogServiceProvider::class,
    Modules\Membership\Providers\MembershipServiceProvider::class,
    Modules\Circulation\Providers\CirculationServiceProvider::class,
];</div>

<h2>3.8 Riwayat Commit Git (Conventional Commits)</h2>
<table>
  <thead>
    <tr>
      <th style="width: 15%;">Commit Hash</th>
      <th style="width: 50%;">Tipe & Pesan Commit</th>
      <th>Keterangan Komponen Modul</th>
    </tr>
  </thead>
  <tbody>
    <tr><td><code>b9d5b44</code></td><td>chore: initialize laravel 13 project for praktikum backend 6</td><td>Inisialisasi repositori Git dan proteksi file AI di .gitignore.</td></tr>
    <tr><td><code>466e7b2</code></td><td>feat(shared): implement ISBN, Denda, exceptions, and contracts</td><td>Pembangunan Value Objects, Exceptions, dan Contracts Interface.</td></tr>
    <tr><td><code>d6054f3</code></td><td>feat(catalog): implement books, hierarchical categories, and service</td><td>Migrasi, Model Buku-Kategori (pivot added_at), dan CatalogService.</td></tr>
    <tr><td><code>fa76089</code></td><td>feat(membership): implement member models, roles, and service</td><td>Migrasi, Model Anggota, Roles, dan MemberService.</td></tr>
    <tr><td><code>7c8a5b4</code></td><td>feat(circulation): implement borrow transactions and BookBorrowed event</td><td>Migrasi Peminjaman, Snapshot Detail, Domain Event, dan Transaksi.</td></tr>
    <tr><td><code>2c153af</code></td><td>feat: register module service providers in bootstrap/providers.php</td><td>Pendaftaran seluruh provider modul ke arsitektur Laravel 13.</td></tr>
    <tr><td><code>58933bf</code></td><td>feat(seeders): implement LibrarySeeder with books and members</td><td>Seeding data uji realistis dengan ISBN-13 tervalidasi.</td></tr>
    <tr><td><code>33a6185</code></td><td>test: add automated feature tests and interactive library demo command</td><td>Pembuatan feature test suite otomatis dan console command demo.</td></tr>
  </tbody>
</table>

<div class="page-break"></div>

<!-- BAB IV -->
<h1>BAB IV: PENGUJIAN SISTEM</h1>
<h2>4.1 Pengujian Relasi Lanjutan (Self-Referencing & Many-to-Many Pivot)</h2>
<div class="code-block">1. PENGUJIAN RELASI LANJUTAN
 a) Self-referencing Category (Parent -> Children):
 - Induk: [Teknologi & Komputer] -> Sub-Kategori: [Pemrograman & Algoritma, Kecerdasan Buatan]
 - Induk: [Sains & Matematika] -> Sub-Kategori: [Fisika Terapan]

 b) Many-to-Many Pivot (Buku <-> Kategori dengan added_at):
 - Judul Buku: Clean Code: A Handbook of Agile Software Craftsmanship
 * Kategori: Teknologi & Komputer (Pivot added_at: 2026-11-08 13:59:22)
 * Kategori: Pemrograman & Algoritma (Pivot added_at: 2026-11-08 13:59:22)</div>

<h2>4.2 Pengujian Query Optimization (Eliminasi Masalah N+1 Query)</h2>
<div class="image-container">
  <img src="images/chart_query_comparison_bw.png" alt="Query Chart">
  <div class="caption">Gambar 4.1 Grafik Perbandingan Eksekusi Query Database (N+1 Query vs Eager Loading)</div>
</div>
<table>
  <thead>
    <tr><th>Metode Pengambilan Data</th><th>Jumlah Data Record</th><th>Jumlah Query SQL</th><th>Status Efisiensi Performa</th></tr>
  </thead>
  <tbody>
    <tr><td><strong>Tanpa Eager Loading (Lazy Loading loop)</strong></td><td>5 Data Peminjaman</td><td>11 Query SQL</td><td>BOROS & LAMBAT (N+1 Query Problem)</td></tr>
    <tr><td><strong>Dengan Eager Loading with(['details', 'member'])</strong></td><td>5 Data Peminjaman</td><td>3 Query SQL</td><td>SANGAT EFISIEN & CEPAT (Teroptimasi)</td></tr>
  </tbody>
</table>

<h2>4.3 Pengujian Query Scopes (Available, Search, ByCategory)</h2>
<p>Query Scopes terbukti berhasil memfilter buku berstatus aktif dan stok > 0, melakukan pencarian fleksibel, serta memfilter berdasarkan ID kategori relasional.</p>

<h2>4.4 Pengujian Database Transaction Berhasil (Atomisitas Pemotongan Stok)</h2>
<p>Saat transaksi peminjaman berhasil, seluruh operasi (pemotongan stok buku, pembuatan header loan, pencatatan snapshot) sukses dikomit bersama.</p>

<h2>4.5 Pengujian Database Transaction Rollback (Stok Kosong)</h2>
<div class="code-block">Mencoba meminjam buku dengan stok kosong ('The Pragmatic Programmer: Your Journey To Mastery', stok: 0)...
[BERHASIL] Exception tertangkap: Stok buku 'The Pragmatic Programmer' tidak mencukupi. Tersedia: 0, diminta: 1.
[VERIFIKASI ROLLBACK] Record Loan sebelum: 5, sesudah: 5
-> DB::transaction() berhasil membatalkan seluruh operasi secara atomik! Konsistensi basis data terjaga 100%.</div>

<h2>4.6 Pengujian Soft Deletes dan Restore Data Terhapus</h2>
<div class="code-block">Menghapus buku #1 ('Clean Code') secara Soft Delete...
- Book::count() (Record Aktif)               : 4 Buku
- Book::withTrashed()->count() (Total Fisik)  : 5 Buku
Mengembalikan buku dengan restore()...
- Book::count() setelah restore             : 5 Buku [DATA PULIH SEMPURNA]</div>

<h2>4.7 Pengujian Value Objects (ISBN & Kalkulasi Denda)</h2>
<p>Pengujian memvalidasi bahwa format ISBN-10 dan ISBN-13 tervalidasi dengan algoritma checksum, serta Value Object Denda secara otomatis mengalikan hari terlambat dengan tarif Rp 2.000/hari.</p>

<h2>4.8 Pengujian Domain Event BookBorrowed & Listener Logging</h2>
<p>Event BookBorrowed berhasil dipancarkan setelah transaksi commit dan ditangkap oleh Listener LogBookBorrowedActivity untuk dicatat pada log sistem.</p>

<h2>4.9 Matriks Hasil Pengujian Otomatis (Automated Testing Pest / PHPUnit)</h2>
<div class="code-block">PASS Tests\\Feature\\LibraryModularDDDTest
✓ test_relasi_lanjutan (Many-to-Many pivot added_at, Self-referencing, HasMany)
✓ test_query_optimization_dan_scopes (Eager loading with() dan Query Scopes)
✓ test_database_transaction_dan_rollback (Atomisitas & Auto-rollback)
✓ test_soft_deletes_dan_restore (Audit trail soft delete & restore)
✓ test_domain_event_dispatched (Event BookBorrowed dipancarkan)
✓ test_value_objects_isbn_dan_denda (Validasi ISBN & kalkulasi denda)

Tests: 6 passed (38 assertions) | Execution Duration: 1.05s</div>

<div class="page-break"></div>

<!-- BAB V -->
<h1>BAB V: KESIMPULAN</h1>
<p>
Berdasarkan seluruh tahapan perancangan, implementasi, dan pengujian yang telah diselesaikan pada Sistem Perpustakaan Modular berbasis Laravel 13, dapat ditarik beberapa kesimpulan pokok:
</p>
<ol>
  <li><strong>Modularitas & Decoupling:</strong> Penerapan Modular Monolith dengan Domain-Driven Design (DDD) berhasil memecah kerumitan logika sistem ke dalam Bounded Context yang jelas (Catalog, Membership, Circulation, Shared Kernel). Ketergantungan langsung antar tabel berhasil dihilangkan melalui perantara Contract (Interface) dan Domain Event.</li>
  <li><strong>Fleksibilitas Relasi Eloquent:</strong> Relasi Many-to-Many dengan pivot custom (added_at) dan Self-referencing hierarkis terbukti sangat ampuh memodelkan hubungan entitas dunia nyata, sedangkan Snapshot Pattern pada detail transaksi menjamin keaslian data historis.</li>
  <li><strong>Efisiensi Query yang Terukur:</strong> Penggunaan Eager Loading terbukti memangkas jumlah eksekusi query dari 11 query menjadi 3 query konstan, mengeliminasi risiko kelambatan sistem akibat masalah N+1 Query.</li>
  <li><strong>Konsistensi Data Transaksional:</strong> Pemanfaatan Database Transaction (DB::transaction) menjamin integritas data secara atomik, di mana kegagalan bisnis pada satu komponen secara otomatis membatalkan seluruh operasi tanpa anomali data.</li>
  <li><strong>Integritas Domain melalui Value Objects:</strong> Pemakaian Value Object (ISBN dan Denda) memperkuat domain model aplikasi dengan memastikan data selalu valid sejak awal pembuatan objek.</li>
</ol>

<h1>LAMPIRAN: TAUTAN REPOSITORY GITHUB</h1>
<p>Seluruh kode sumber, riwayat commit Git, modul, dan script pengujian dapat diakses pada repositori publik berikut:</p>
<p style="font-size: 11pt; font-weight: bold; font-family: 'Consolas', monospace;">
  🔗 <a href="https://github.com/panjiprasetyaa/praktikum-backend-6.git">https://github.com/panjiprasetyaa/praktikum-backend-6.git</a>
</p>

</body>
</html>
"""

html_path = r"d:\project6\laporan\LAPORAN_PRAKTIKUM_PERTEMUAN_6.html"
with open(html_path, "w", encoding="utf-8") as f:
    f.write(html_content)
print("HTML successfully created:", html_path)

pdf_path = r"d:\project6\laporan\LAPORAN_PRAKTIKUM_PERTEMUAN_6.pdf"
chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
if os.path.exists(chrome_path):
    cmd = [
        chrome_path,
        "--headless=new",
        "--disable-gpu",
        f"--print-to-pdf={pdf_path}",
        "--no-pdf-header-footer",
        html_path
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if os.path.exists(pdf_path) and os.path.getsize(pdf_path) > 0:
        print(f"PDF successfully created: {pdf_path} (Size: {os.path.getsize(pdf_path)} bytes)")
    else:
        print(f"PDF creation failed: {res.stderr}")
