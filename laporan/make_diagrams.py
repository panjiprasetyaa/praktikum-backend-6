import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Set global monochrome style
plt.rcParams['font.sans-serif'] = 'Arial'
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['figure.dpi'] = 300

out_dir = r"d:\project6\laporan\images"
os.makedirs(out_dir, exist_ok=True)

# ==============================================================================
# 1. Bounded Context Diagram (Hitam Putih / Grayscale)
# ==============================================================================
fig, ax = plt.subplots(figsize=(10, 6.5), facecolor='white')
ax.set_facecolor('white')
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.axis('off')

# Shared Kernel Box (Top)
rect_sk = patches.FancyBboxPatch((10, 68), 80, 26, boxstyle="round,pad=1.5",
                                 facecolor="#f5f5f5", edgecolor="black", linewidth=1.5)
ax.add_patch(rect_sk)
ax.text(50, 90, "SHARED KERNEL (app/Modules/Shared)", fontsize=11, fontweight='bold', ha='center', color='black')
ax.text(25, 76, "Value Objects:\n• ISBN (Format Validator)\n• Denda (Tarif & Kalkulasi)",
        fontsize=9, ha='center', va='center', bbox=dict(boxstyle="square,pad=0.5", facecolor='white', edgecolor='black', lw=1))
ax.text(50, 76, "Contracts (Interfaces):\n• BookServiceInterface\n• MemberServiceInterface",
        fontsize=9, ha='center', va='center', bbox=dict(boxstyle="square,pad=0.5", facecolor='white', edgecolor='black', lw=1))
ax.text(75, 76, "Domain Exceptions:\n• InsufficientStockException\n• MemberNotEligibleException",
        fontsize=9, ha='center', va='center', bbox=dict(boxstyle="square,pad=0.5", facecolor='white', edgecolor='black', lw=1))

# Catalog Context Box (Bottom Left)
rect_cat = patches.FancyBboxPatch((5, 10), 28, 48, boxstyle="round,pad=1",
                                  facecolor="#ffffff", edgecolor="black", linewidth=1.5)
ax.add_patch(rect_cat)
ax.text(19, 54, "CATALOG CONTEXT", fontsize=10, fontweight='bold', ha='center', color='black')
ax.text(19, 50, "(app/Modules/Catalog)", fontsize=8, fontstyle='italic', ha='center', color='black')
cat_text = "Aggregate Root:\n• Book (Buku)\n\nEntities:\n• Category (Self-Ref)\n• Author & Publisher\n\nPivot Table:\n• book_category (added_at)\n\nService:\n• CatalogService"
ax.text(19, 30, cat_text, fontsize=8.5, ha='center', va='center',
        bbox=dict(boxstyle="square,pad=0.5", facecolor='#f9f9f9', edgecolor='black', lw=0.8))

# Membership Context Box (Bottom Center)
rect_mem = patches.FancyBboxPatch((36, 10), 28, 48, boxstyle="round,pad=1",
                                  facecolor="#ffffff", edgecolor="black", linewidth=1.5)
ax.add_patch(rect_mem)
ax.text(50, 54, "MEMBERSHIP CONTEXT", fontsize=10, fontweight='bold', ha='center', color='black')
ax.text(50, 50, "(app/Modules/Membership)", fontsize=8, fontstyle='italic', ha='center', color='black')
mem_text = "Aggregate Root:\n• Member (Anggota)\n\nEntity:\n• Role (Hak Akses)\n\nPivot Table:\n• member_role\n\nService:\n• MemberService\n\nRule Invariant:\n• Status harus 'active'"
ax.text(50, 30, mem_text, fontsize=8.5, ha='center', va='center',
        bbox=dict(boxstyle="square,pad=0.5", facecolor='#f9f9f9', edgecolor='black', lw=0.8))

# Circulation Context Box (Bottom Right)
rect_circ = patches.FancyBboxPatch((67, 10), 28, 48, boxstyle="round,pad=1",
                                   facecolor="#ffffff", edgecolor="black", linewidth=1.5)
ax.add_patch(rect_circ)
ax.text(81, 54, "CIRCULATION CONTEXT", fontsize=10, fontweight='bold', ha='center', color='black')
ax.text(81, 50, "(app/Modules/Circulation)", fontsize=8, fontstyle='italic', ha='center', color='black')
circ_text = "Aggregate Root:\n• Loan (Peminjaman)\n\nEntities:\n• LoanDetail (Snapshot)\n• Fine (Denda)\n\nService:\n• CirculationService\n\nDomain Event:\n• BookBorrowed (Event)\n• LogBookBorrowed (Listener)"
ax.text(81, 30, circ_text, fontsize=8.5, ha='center', va='center',
        bbox=dict(boxstyle="square,pad=0.5", facecolor='#f9f9f9', edgecolor='black', lw=0.8))

# Connecting Arrows (Monochrome)
# Circulation to Catalog via Contract
ax.annotate("", xy=(33, 40), xytext=(67, 40),
            arrowprops=dict(arrowstyle="->", color="black", lw=1.5))
ax.text(50, 42, "Cek & Kurangi Stok (via Contract)", fontsize=7.5, ha='center', backgroundcolor='white')

# Circulation to Membership via Contract
ax.annotate("", xy=(64, 25), xytext=(67, 25),
            arrowprops=dict(arrowstyle="->", color="black", lw=1.5))
ax.text(65.5, 27, "Validasi Anggota", fontsize=7.5, ha='center', backgroundcolor='white')

plt.title("Gambar 2.1 Diagram Bounded Context Sistem Perpustakaan Modular (DDD)",
          fontsize=12, fontweight='bold', pad=15, color='black')
plt.tight_layout()
plt.savefig(os.path.join(out_dir, "diagram_bounded_context_bw.png"), bbox_inches='tight')
plt.close()
print("1. Bounded Context Diagram saved.")

# ==============================================================================
# 2. Database Transaction Flowchart (Hitam Putih)
# ==============================================================================
fig, ax = plt.subplots(figsize=(8, 10), facecolor='white')
ax.set_facecolor('white')
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.axis('off')

def draw_box(x, y, text, w=60, h=6, facecolor='white', style="round"):
    if style == "round":
        box = patches.FancyBboxPatch((x - w/2, y - h/2), w, h, boxstyle="round,pad=0.8",
                                     facecolor=facecolor, edgecolor="black", linewidth=1.2)
    elif style == "diamond":
        box = patches.RegularPolygon((x, y), numVertices=4, radius=h*1.2, orientation=0,
                                     facecolor=facecolor, edgecolor="black", linewidth=1.2)
    else:
        box = patches.Rectangle((x - w/2, y - h/2), w, h,
                                facecolor=facecolor, edgecolor="black", linewidth=1.2)
    ax.add_patch(box)
    ax.text(x, y, text, fontsize=9, ha='center', va='center', color='black', fontweight='bold' if 'Mulai' in text or 'Selesai' in text or 'Commit' in text or 'Rollback' in text else 'normal')

draw_box(50, 95, "Mulai: Peminjaman Buku (CirculationService)", w=64, h=5, facecolor="#e6e6e6")
draw_box(50, 86, "DB::transaction(function() { ... }) Dimulai", w=56, h=5, facecolor="white")
draw_box(50, 77, "Validasi Kelayakan Anggota via MemberServiceInterface", w=66, h=5, facecolor="white")
draw_box(50, 68, "Buat Header Loan (Status: 'borrowed', Kode Unik)", w=62, h=5, facecolor="white")
draw_box(50, 59, "Iterasi Setiap Buku yang Dipinjam", w=48, h=5, facecolor="#f0f0f0")
draw_box(50, 50, "Cek Ketersediaan Stok via BookServiceInterface", w=62, h=5, facecolor="white")
draw_box(50, 40, "Apakah Stok Tersedia? (stock >= 1)", w=46, h=6, facecolor="white")
draw_box(50, 29, "Simpan Snapshot (Judul & ISBN) ke LoanDetail", w=60, h=5, facecolor="white")
draw_box(50, 20, "Kurangi Stok Buku via CatalogService::reduceStock()", w=64, h=5, facecolor="white")
draw_box(50, 11, "Dispatch Domain Event: BookBorrowed", w=54, h=5, facecolor="#f0f0f0")
draw_box(50, 3, "Commit Database Transaction & Return Loan (Sukses)", w=64, h=5, facecolor="#e6e6e6")

# Rollback Box on Right
rect_rb = patches.FancyBboxPatch((78, 36), 20, 14, boxstyle="round,pad=0.8",
                                 facecolor="#ffffff", edgecolor="black", linewidth=1.5, linestyle="--")
ax.add_patch(rect_rb)
ax.text(88, 43, "ROLLBACK\nTRANSAKSI\n(Atomik)", fontsize=8.5, ha='center', va='center', fontweight='bold', color='black')

# Arrows
ax.annotate("", xy=(50, 88.5), xytext=(50, 92.5), arrowprops=dict(arrowstyle="->", color="black", lw=1.2))
ax.annotate("", xy=(50, 79.5), xytext=(50, 83.5), arrowprops=dict(arrowstyle="->", color="black", lw=1.2))
ax.annotate("", xy=(50, 70.5), xytext=(50, 74.5), arrowprops=dict(arrowstyle="->", color="black", lw=1.2))
ax.annotate("", xy=(50, 61.5), xytext=(50, 65.5), arrowprops=dict(arrowstyle="->", color="black", lw=1.2))
ax.annotate("", xy=(50, 52.5), xytext=(50, 56.5), arrowprops=dict(arrowstyle="->", color="black", lw=1.2))
ax.annotate("", xy=(50, 43), xytext=(50, 47.5), arrowprops=dict(arrowstyle="->", color="black", lw=1.2))

# Conditional branching
ax.annotate("", xy=(50, 31.5), xytext=(50, 37), arrowprops=dict(arrowstyle="->", color="black", lw=1.2))
ax.text(52, 34, "Ya", fontsize=8, fontweight='bold')

ax.annotate("", xy=(78, 40), xytext=(73, 40), arrowprops=dict(arrowstyle="->", color="black", lw=1.2))
ax.text(74, 41.5, "Tidak", fontsize=8, fontweight='bold')

ax.annotate("", xy=(50, 22.5), xytext=(50, 26.5), arrowprops=dict(arrowstyle="->", color="black", lw=1.2))
ax.annotate("", xy=(50, 13.5), xytext=(50, 17.5), arrowprops=dict(arrowstyle="->", color="black", lw=1.2))
ax.annotate("", xy=(50, 5.5), xytext=(50, 8.5), arrowprops=dict(arrowstyle="->", color="black", lw=1.2))

plt.title("Gambar 2.2 Alur Eksekusi Database Transaction dan Rollback (Monochrome)",
          fontsize=11, fontweight='bold', pad=12, color='black')
plt.tight_layout()
plt.savefig(os.path.join(out_dir, "diagram_transaction_flow_bw.png"), bbox_inches='tight')
plt.close()
print("2. Transaction Flowchart saved.")

# ==============================================================================
# 3. Entity Relationship Diagram (ERD) Monochrome
# ==============================================================================
fig, ax = plt.subplots(figsize=(11, 7.5), facecolor='white')
ax.set_facecolor('white')
ax.set_xlim(0, 110)
ax.set_ylim(0, 100)
ax.axis('off')

def draw_table(x, y, title, fields, w=22, h=22):
    rect = patches.Rectangle((x, y - h), w, h, facecolor='white', edgecolor='black', linewidth=1.2)
    ax.add_patch(rect)
    header = patches.Rectangle((x, y - 4), w, 4, facecolor='#e6e6e6', edgecolor='black', linewidth=1.2)
    ax.add_patch(header)
    ax.text(x + w/2, y - 2.2, title, fontsize=9, fontweight='bold', ha='center', va='center', color='black')
    text_content = "\n".join(fields)
    ax.text(x + 1, y - 5, text_content, fontsize=7.5, va='top', ha='left', family='monospace', color='black')

# 1. CATEGORIES
draw_table(5, 95, "CATEGORIES", [
    "+ id [PK]",
    "- name",
    "- slug [UQ]",
    "- parent_id [FK->categories]",
    "- deleted_at [SoftDelete]"
], w=26, h=20)

# 2. BOOK_CATEGORY (Pivot)
draw_table(42, 95, "BOOK_CATEGORY (Pivot)", [
    "+ book_id [PK, FK]",
    "+ category_id [PK, FK]",
    "- added_at [Timestamp]"
], w=26, h=14)

# 3. BOOKS
draw_table(78, 95, "BOOKS", [
    "+ id [PK]",
    "- isbn [UQ]",
    "- title",
    "- slug [UQ]",
    "- stock [Int]",
    "- is_active [Bool]",
    "- deleted_at [SoftDelete]"
], w=26, h=24)

# 4. MEMBERS
draw_table(5, 55, "MEMBERS", [
    "+ id [PK]",
    "- member_code [UQ]",
    "- name",
    "- email [UQ]",
    "- status [active/suspended]",
    "- max_loans [Int]",
    "- deleted_at [SoftDelete]"
], w=26, h=25)

# 5. ROLES & MEMBER_ROLE
draw_table(5, 20, "ROLES", [
    "+ id [PK]",
    "- name",
    "- slug [UQ]"
], w=14, h=12)

draw_table(23, 20, "MEMBER_ROLE", [
    "+ member_id [PK, FK]",
    "+ role_id [PK, FK]"
], w=18, h=12)

# 6. LOANS
draw_table(42, 55, "LOANS", [
    "+ id [PK]",
    "- loan_code [UQ]",
    "- member_id [FK->members]",
    "- borrowed_at [Timestamp]",
    "- due_date [Timestamp]",
    "- returned_at [Timestamp]",
    "- status [borrowed/ret/over]",
    "- deleted_at [SoftDelete]"
], w=28, h=27)

# 7. LOAN_DETAILS
draw_table(78, 55, "LOAN_DETAILS", [
    "+ id [PK]",
    "- loan_id [FK->loans]",
    "- book_id [Ref->books]",
    "- book_title [SNAPSHOT]",
    "- book_isbn [SNAPSHOT]",
    "- returned_at [Timestamp]"
], w=26, h=22)

# 8. FINES
draw_table(42, 18, "FINES", [
    "+ id [PK]",
    "- loan_id [FK->loans]",
    "- days_overdue [Int]",
    "- daily_rate [Decimal]",
    "- total_fine [Decimal]",
    "- is_paid [Bool]"
], w=28, h=18)

# Connecting Lines
# Categories -> Categories (Self-ref)
ax.annotate("", xy=(5, 93), xytext=(2, 90), arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=-0.4", color="black", lw=1))
ax.annotate("", xy=(2, 90), xytext=(5, 87), arrowprops=dict(connectionstyle="arc3,rad=-0.4", color="black", lw=1))
ax.text(0, 90, "parent_id\n(Self-Ref)", fontsize=6.5, ha='right', va='center')

# Categories <-> Book_Category <-> Books
ax.plot([31, 42], [88, 88], 'k-', lw=1.2)
ax.plot([68, 78], [88, 88], 'k-', lw=1.2)
ax.text(36.5, 89.5, "1:N", fontsize=7, ha='center')
ax.text(73, 89.5, "N:1", fontsize=7, ha='center')

# Loans <-> Loan_Details
ax.plot([70, 78], [44, 44], 'k-', lw=1.2)
ax.text(74, 45.5, "1:N", fontsize=7, ha='center')

# Members <-> Loans
ax.plot([31, 42], [44, 44], 'k-', lw=1.2)
ax.text(36.5, 45.5, "1:N", fontsize=7, ha='center')

# Loans <-> Fines
ax.plot([56, 56], [28, 18], 'k-', lw=1.2)
ax.text(57.5, 23, "1:N", fontsize=7, va='center')

# Members <-> Member_Role <-> Roles
ax.plot([19, 23], [14, 14], 'k-', lw=1.2)
ax.plot([14, 14], [30, 20], 'k-', lw=1.2)

# Cross context snapshot line Books -> Loan_Details
ax.plot([91, 91], [71, 55], 'k--', lw=1.2)
ax.text(92, 63, "Snapshot Data\n(Cross-Context)", fontsize=7, va='center', fontstyle='italic')

plt.title("Gambar 2.3 Entity Relationship Diagram (ERD) Perpustakaan Modular (Monochrome)",
          fontsize=11, fontweight='bold', pad=12, color='black')
plt.tight_layout()
plt.savefig(os.path.join(out_dir, "diagram_erd_bw.png"), bbox_inches='tight')
plt.close()
print("3. ERD saved.")

# ==============================================================================
# 4. Query Comparison Bar Chart (Monochrome)
# ==============================================================================
fig, ax = plt.subplots(figsize=(7, 4.5), facecolor='white')
ax.set_facecolor('white')

methods = ['Lazy Loading (N+1 Query)\n[Tanpa with()]', 'Eager Loading\n[with(["details", "member"])]']
queries = [11, 3]
bars = ax.bar(methods, queries, color=['#b0b0b0', '#202020'], edgecolor='black', width=0.45, linewidth=1.2)

ax.set_ylabel('Jumlah Eksekusi Query Database (SQL)', fontsize=10, fontweight='bold', color='black')
ax.set_title('Gambar 4.1 Perbandingan Eksekusi Query Database (N+1 vs Eager Loading)',
             fontsize=11, fontweight='bold', pad=15, color='black')
ax.set_ylim(0, 14)
ax.grid(axis='y', linestyle='--', alpha=0.5, color='gray')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

for bar in bars:
    yval = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, yval + 0.4, f"{yval} Query",
            ha='center', va='bottom', fontsize=10, fontweight='bold', color='black')

ax.text(0, 11.8, "Boros (11 Query untuk 5 Record)", ha='center', fontsize=8, color='#444444')
ax.text(1, 3.8, "Efisien (Hanya 3 Query Konstan)", ha='center', fontsize=8, color='#111111')

plt.tight_layout()
plt.savefig(os.path.join(out_dir, "chart_query_comparison_bw.png"), bbox_inches='tight')
plt.close()
print("4. Query comparison chart saved.")
