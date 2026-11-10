<x-app-layout>
    <x-slot name="header">
        <div class="flex justify-between items-center">
            <h2 class="font-semibold text-xl text-gray-800 leading-tight">
                {{ __('Trash & Restore Buku (Khusus Admin)') }}
            </h2>
            <a href="{{ route('library.books.index') }}" class="text-sm text-gray-600 hover:text-gray-900">
                &larr; Kembali ke Katalog Aktif
            </a>
        </div>
    </x-slot>

    <div class="py-8">
        <div class="max-w-7xl mx-auto sm:px-6 lg:px-8 space-y-4">
            @if (session('success'))
                <div class="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded">
                    {{ session('success') }}
                </div>
            @endif

            <div class="bg-white overflow-hidden shadow-sm sm:rounded-lg p-6">
                <table class="min-w-full border border-gray-200 text-sm">
                    <thead>
                        <tr class="bg-gray-100 text-gray-700 uppercase text-xs">
                            <th class="py-3 px-4 text-left border-b">ISBN</th>
                            <th class="py-3 px-4 text-left border-b">Judul Buku</th>
                            <th class="py-3 px-4 text-left border-b">Dihapus Pada (<code>deleted_at</code>)</th>
                            <th class="py-3 px-4 text-center border-b">Aksi Admin</th>
                        </tr>
                    </thead>
                    <tbody class="divide-y divide-gray-200">
                        @forelse ($trashedBooks as $book)
                            <tr>
                                <td class="py-3 px-4 font-mono text-xs">{{ $book->isbn }}</td>
                                <td class="py-3 px-4 font-semibold">{{ $book->title }}</td>
                                <td class="py-3 px-4 text-xs text-gray-500">{{ $book->deleted_at }}</td>
                                <td class="py-3 px-4 text-center">
                                    <form action="{{ route('library.books.restore', $book->id) }}" method="POST">
                                        @csrf
                                        <button type="submit" class="bg-green-600 hover:bg-green-800 text-white font-semibold py-1 px-3 rounded text-xs">
                                            Restore Data
                                        </button>
                                    </form>
                                </td>
                            </tr>
                        @empty
                            <tr>
                                <td colspan="4" class="py-6 text-center text-gray-500">Tidak ada data buku yang dihapus (Trash kosong).</td>
                            </tr>
                        @endforelse
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</x-app-layout>
