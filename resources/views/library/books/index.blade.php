<x-app-layout>
    <x-slot name="header">
        <div class="flex flex-wrap justify-between items-center gap-3">
            <div>
                <h2 class="font-semibold text-xl text-gray-800 leading-tight">
                    {{ __('Katalog Buku Perpustakaan (Catalog Context)') }}
                </h2>
                <p class="text-xs text-gray-500 mt-1">
                    Eager Loading <code>Book::with('categories')</code> aktif — Total SQL dieksekusi: <span class="font-bold text-gray-800">{{ $queryCount }} Query</span>
                </p>
            </div>
            <div class="flex items-center space-x-2">
                @if(Auth::user()->role === 'admin')
                    <a href="{{ route('library.books.trash') }}" class="bg-gray-600 hover:bg-gray-800 text-white text-sm font-semibold py-2 px-4 rounded">
                        Trash / Restore (Admin)
                    </a>
                @endif
                <a href="{{ route('library.books.create') }}" class="bg-blue-600 hover:bg-blue-800 text-white text-sm font-semibold py-2 px-4 rounded">
                    + Tambah Buku
                </a>
            </div>
        </div>
    </x-slot>

    <div class="py-8">
        <div class="max-w-7xl mx-auto sm:px-6 lg:px-8 space-y-6">
            @if (session('success'))
                <div class="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded">
                    {{ session('success') }}
                </div>
            @endif

            {{-- Filter & Pencarian (Query Scopes) --}}
            <div class="bg-white shadow-sm sm:rounded-lg p-6">
                <form method="GET" action="{{ route('library.books.index') }}" class="grid grid-cols-1 md:grid-cols-4 gap-4 items-end">
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-1">Pencarian (Scope: <code>search</code>)</label>
                        <input type="text" name="search" value="{{ request('search') }}" placeholder="Judul, pengarang, ISBN..."
                            class="w-full rounded-md border-gray-300 shadow-sm text-sm">
                    </div>

                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-1">Kategori (Scope: <code>byCategory</code>)</label>
                        <select name="category_id" class="w-full rounded-md border-gray-300 shadow-sm text-sm">
                            <option value="">-- Semua Kategori --</option>
                            @foreach($categories as $parent)
                                <option value="{{ $parent->id }}" @selected(request('category_id') == $parent->id)>
                                    {{ $parent->name }}
                                </option>
                                @foreach($parent->children as $child)
                                    <option value="{{ $child->id }}" @selected(request('category_id') == $child->id)>
                                        &nbsp;&nbsp;↳ {{ $child->name }}
                                    </option>
                                @endforeach
                            @endforeach
                        </select>
                    </div>

                    <div class="flex items-center pb-2">
                        <input type="checkbox" id="available" name="available" value="1" @checked(request('available'))
                            class="rounded border-gray-300 text-blue-600 shadow-sm">
                        <label for="available" class="ms-2 text-sm text-gray-700">
                            Hanya Stok Tersedia (<code>available</code>)
                        </label>
                    </div>

                    <div class="flex space-x-2">
                        <button type="submit" class="bg-gray-800 hover:bg-gray-900 text-white text-sm font-semibold py-2 px-4 rounded">
                            Filter
                        </button>
                        <a href="{{ route('library.books.index') }}" class="bg-gray-200 hover:bg-gray-300 text-gray-800 text-sm font-semibold py-2 px-4 rounded">
                            Reset
                        </a>
                    </div>
                </form>
            </div>

            {{-- Tabel Daftar Buku --}}
            <div class="bg-white overflow-hidden shadow-sm sm:rounded-lg">
                <div class="p-6 text-gray-900 overflow-x-auto">
                    <table class="min-w-full border border-gray-200 text-sm">
                        <thead>
                            <tr class="bg-gray-100 text-gray-700 uppercase text-xs">
                                <th class="py-3 px-4 text-left border-b">ISBN</th>
                                <th class="py-3 px-4 text-left border-b">Judul & Pengarang</th>
                                <th class="py-3 px-4 text-left border-b">Kategori (Pivot <code>added_at</code>)</th>
                                <th class="py-3 px-4 text-center border-b">Stok</th>
                                <th class="py-3 px-4 text-center border-b">Aksi</th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-gray-200">
                            @forelse ($books as $book)
                                <tr class="hover:bg-gray-50">
                                    <td class="py-3 px-4 font-mono text-xs">{{ $book->isbn }}</td>
                                    <td class="py-3 px-4">
                                        <div class="font-semibold text-gray-900">{{ $book->title }}</div>
                                        <div class="text-xs text-gray-500">{{ $book->author }} — {{ $book->publisher }}</div>
                                    </td>
                                    <td class="py-3 px-4">
                                        <div class="flex flex-wrap gap-1">
                                            @foreach($book->categories as $cat)
                                                <span class="inline-block bg-gray-100 border border-gray-300 text-gray-700 text-xs px-2 py-0.5 rounded"
                                                    title="Added at: {{ $cat->pivot->added_at }}">
                                                    {{ $cat->name }}
                                                </span>
                                            @endforeach
                                        </div>
                                    </td>
                                    <td class="py-3 px-4 text-center">
                                        @if($book->stock > 0)
                                            <span class="bg-green-100 text-green-800 font-bold px-2.5 py-0.5 rounded text-xs">{{ $book->stock }}</span>
                                        @else
                                            <span class="bg-red-100 text-red-800 font-bold px-2.5 py-0.5 rounded text-xs">0 (Habis)</span>
                                        @endif
                                    </td>
                                    <td class="py-3 px-4 text-center">
                                        <form action="{{ route('library.books.destroy', $book->id) }}" method="POST"
                                            onsubmit="return confirm('Soft delete buku ini?');">
                                            @csrf
                                            @method('DELETE')
                                            <button type="submit" class="text-red-600 hover:text-red-800 font-semibold text-xs">
                                                Soft Delete
                                            </button>
                                        </form>
                                    </td>
                                </tr>
                            @empty
                                <tr>
                                    <td colspan="5" class="py-6 text-center text-gray-500">Tidak ada buku yang cocok dengan kriteria pencarian.</td>
                                </tr>
                            @endforelse
                        </tbody>
                    </table>

                    <div class="mt-4">
                        {{ $books->links() }}
                    </div>
                </div>
            </div>
        </div>
    </div>
</x-app-layout>
