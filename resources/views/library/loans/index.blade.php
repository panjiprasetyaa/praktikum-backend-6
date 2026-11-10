<x-app-layout>
    <x-slot name="header">
        <div class="flex flex-wrap justify-between items-center gap-3">
            <div>
                <h2 class="font-semibold text-xl text-gray-800 leading-tight">
                    {{ __('Sirkulasi Peminjaman & Pengembalian (Circulation Context)') }}
                </h2>
                <p class="text-xs text-gray-500 mt-1">
                    Eager Loading <code>Loan::with(['member', 'details', 'fines'])</code> aktif — Total SQL dieksekusi: <span class="font-bold text-gray-800">{{ $queryCount }} Query</span>
                </p>
            </div>
            @if(Auth::user()->role === 'admin')
                <a href="{{ route('library.loans.trash') }}" class="bg-gray-600 hover:bg-gray-800 text-white text-sm font-semibold py-2 px-4 rounded">
                    Trash / Restore (Admin)
                </a>
            @endif
        </div>
    </x-slot>

    <div class="py-8">
        <div class="max-w-7xl mx-auto sm:px-6 lg:px-8 space-y-6">
            @if (session('success'))
                <div class="bg-green-100 border border-green-400 text-green-800 px-4 py-3 rounded">
                    {{ session('success') }}
                </div>
            @endif

            @if (session('error'))
                <div class="bg-red-100 border border-red-400 text-red-800 px-4 py-3 rounded font-semibold">
                    {{ session('error') }}
                </div>
            @endif

            {{-- Form Peminjaman Buku (Database Transaction) --}}
            <div class="bg-white shadow-sm sm:rounded-lg p-6">
                <h3 class="font-semibold text-gray-800 mb-3 text-base">
                    Buat Transaksi Peminjaman Baru (<code>DB::transaction</code> Atomik)
                </h3>
                <form method="POST" action="{{ route('library.loans.store') }}" class="space-y-4">
                    @csrf
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div>
                            <label class="block text-sm font-medium text-gray-700 mb-1">Pilih Anggota Peminjam</label>
                            <select name="member_id" required class="w-full rounded-md border-gray-300 shadow-sm text-sm">
                                @foreach($members as $m)
                                    <option value="{{ $m->id }}">
                                        [{{ $m->member_code }}] {{ $m->name }} — Status: {{ strtoupper($m->status) }}
                                    </option>
                                @endforeach
                            </select>
                        </div>
                        <div>
                            <label class="block text-sm font-medium text-gray-700 mb-1">Durasi Pinjam (Hari)</label>
                            <input type="number" name="loan_days" value="7" min="1" max="30"
                                class="w-32 rounded-md border-gray-300 shadow-sm text-sm">
                        </div>
                    </div>

                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-2">
                            Pilih Buku yang Dipinjam <span class="text-xs text-gray-500">(Pilih buku stok 0 untuk menguji Auto-Rollback Transaction)</span>
                        </label>
                        <div class="grid grid-cols-1 md:grid-cols-2 gap-2 max-h-48 overflow-y-auto border border-gray-200 p-3 rounded">
                            @foreach($books as $b)
                                <label class="inline-flex items-center text-sm text-gray-700 p-1 hover:bg-gray-50 rounded">
                                    <input type="checkbox" name="book_ids[]" value="{{ $b->id }}" class="rounded border-gray-300 text-blue-600">
                                    <span class="ms-2">
                                        <strong>{{ $b->title }}</strong>
                                        <span class="text-xs {{ $b->stock > 0 ? 'text-green-700' : 'text-red-600 font-bold' }}">
                                            (Stok: {{ $b->stock }})
                                        </span>
                                    </span>
                                </label>
                            @endforeach
                        </div>
                    </div>

                    <button type="submit" class="bg-blue-600 hover:bg-blue-800 text-white font-semibold py-2 px-5 rounded text-sm">
                        Proses Peminjaman (Jalankan DB Transaction)
                    </button>
                </form>
            </div>

            {{-- Tabel Riwayat Peminjaman --}}
            <div class="bg-white overflow-hidden shadow-sm sm:rounded-lg p-6 overflow-x-auto">
                <h3 class="font-semibold text-gray-800 mb-3 text-base">Daftar Riwayat Peminjaman</h3>
                <table class="min-w-full border border-gray-200 text-sm">
                    <thead>
                        <tr class="bg-gray-100 text-gray-700 uppercase text-xs">
                            <th class="py-3 px-4 text-left border-b">Kode Pinjam</th>
                            <th class="py-3 px-4 text-left border-b">Peminjam</th>
                            <th class="py-3 px-4 text-left border-b">Detail Buku (Snapshot)</th>
                            <th class="py-3 px-4 text-center border-b">Status</th>
                            <th class="py-3 px-4 text-center border-b">Aksi</th>
                        </tr>
                    </thead>
                    <tbody class="divide-y divide-gray-200">
                        @forelse ($loans as $loan)
                            <tr class="hover:bg-gray-50">
                                <td class="py-3 px-4">
                                    <div class="font-mono text-xs font-bold">{{ $loan->loan_code }}</div>
                                    <div class="text-xs text-gray-500">Pinjam: {{ $loan->borrowed_at->format('d M Y') }}</div>
                                    <div class="text-xs text-gray-500">Tempo: {{ $loan->due_date->format('d M Y') }}</div>
                                </td>
                                <td class="py-3 px-4">
                                    <div class="font-semibold">{{ $loan->member?->name ?? 'Anggota Dihapus' }}</div>
                                    <div class="text-xs text-gray-500">{{ $loan->member?->member_code }}</div>
                                </td>
                                <td class="py-3 px-4">
                                    <ul class="list-disc list-inside text-xs space-y-1">
                                        @foreach($loan->details as $detail)
                                            <li>
                                                <span class="font-semibold">{{ $detail->book_title }}</span>
                                                <span class="text-gray-500 font-mono">({{ $detail->book_isbn }})</span>
                                            </li>
                                        @endforeach
                                    </ul>
                                </td>
                                <td class="py-3 px-4 text-center">
                                    @if($loan->status === 'borrowed')
                                        <span class="bg-yellow-100 text-yellow-800 font-bold px-2.5 py-0.5 rounded text-xs">Borrowed</span>
                                    @elseif($loan->status === 'returned')
                                        <span class="bg-green-100 text-green-800 font-bold px-2.5 py-0.5 rounded text-xs">Returned</span>
                                    @else
                                        <span class="bg-red-100 text-red-800 font-bold px-2.5 py-0.5 rounded text-xs">{{ ucfirst($loan->status) }}</span>
                                    @endif

                                    @if($loan->fines->isNotEmpty())
                                        <div class="text-xs text-red-600 mt-1 font-semibold">
                                            Denda: Rp {{ number_format($loan->fines->sum('total_fine'), 0, ',', '.') }}
                                        </div>
                                    @endif
                                </td>
                                <td class="py-3 px-4 text-center space-y-1">
                                    @if($loan->status === 'borrowed')
                                        <form action="{{ route('library.loans.return', $loan->id) }}" method="POST">
                                            @csrf
                                            <button type="submit" class="bg-green-600 hover:bg-green-800 text-white font-semibold py-1 px-2.5 rounded text-xs">
                                                Kembalikan
                                            </button>
                                        </form>
                                    @endif
                                    <form action="{{ route('library.loans.destroy', $loan->id) }}" method="POST"
                                        onsubmit="return confirm('Soft delete data peminjaman ini?');">
                                        @csrf
                                        @method('DELETE')
                                        <button type="submit" class="text-red-600 hover:text-red-800 font-semibold text-xs">
                                            Soft Delete
                                        </button>
                                    </form>
                                </td>
                            </tr>
                        @empty
                            <tr><td colspan="5" class="py-4 text-center text-gray-500">Belum ada transaksi peminjaman.</td></tr>
                        @endforelse
                    </tbody>
                </table>
                <div class="mt-4">{{ $loans->links() }}</div>
            </div>
        </div>
    </div>
</x-app-layout>
