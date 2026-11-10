<x-app-layout>
    <x-slot name="header">
        <div class="flex justify-between items-center">
            <h2 class="font-semibold text-xl text-gray-800 leading-tight">
                {{ __('Tambah Buku Baru (Validasi Value Object ISBN)') }}
            </h2>
            <a href="{{ route('library.books.index') }}" class="text-sm text-gray-600 hover:text-gray-900">
                &larr; Kembali ke Katalog
            </a>
        </div>
    </x-slot>

    <div class="py-8">
        <div class="max-w-3xl mx-auto sm:px-6 lg:px-8">
            <div class="bg-white shadow-sm sm:rounded-lg p-6">
                <form method="POST" action="{{ route('library.books.store') }}" class="space-y-4">
                    @csrf

                    <div>
                        <label class="block text-sm font-medium text-gray-700">ISBN (Contoh Valid: 978-0-13-110362-7)</label>
                        <input type="text" name="isbn" value="{{ old('isbn') }}" required
                            class="mt-1 w-full rounded-md border-gray-300 shadow-sm text-sm">
                        @error('isbn')
                            <p class="text-red-600 text-xs mt-1">{{ $message }}</p>
                        @enderror
                    </div>

                    <div>
                        <label class="block text-sm font-medium text-gray-700">Judul Buku</label>
                        <input type="text" name="title" value="{{ old('title') }}" required
                            class="mt-1 w-full rounded-md border-gray-300 shadow-sm text-sm">
                    </div>

                    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div>
                            <label class="block text-sm font-medium text-gray-700">Pengarang</label>
                            <input type="text" name="author" value="{{ old('author') }}" required
                                class="mt-1 w-full rounded-md border-gray-300 shadow-sm text-sm">
                        </div>
                        <div>
                            <label class="block text-sm font-medium text-gray-700">Penerbit</label>
                            <input type="text" name="publisher" value="{{ old('publisher') }}"
                                class="mt-1 w-full rounded-md border-gray-300 shadow-sm text-sm">
                        </div>
                    </div>

                    <div>
                        <label class="block text-sm font-medium text-gray-700">Stok Tersedia</label>
                        <input type="number" name="stock" value="{{ old('stock', 5) }}" min="0" required
                            class="mt-1 w-32 rounded-md border-gray-300 shadow-sm text-sm">
                    </div>

                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-2">Kategori Buku</label>
                        <div class="grid grid-cols-2 gap-2">
                            @foreach($categories as $cat)
                                <label class="inline-flex items-center text-sm text-gray-700">
                                    <input type="checkbox" name="category_ids[]" value="{{ $cat->id }}" class="rounded border-gray-300 text-blue-600">
                                    <span class="ms-2">{{ $cat->name }}</span>
                                </label>
                            @endforeach
                        </div>
                    </div>

                    <div class="pt-4">
                        <button type="submit" class="bg-blue-600 hover:bg-blue-800 text-white font-semibold py-2 px-6 rounded text-sm">
                            Simpan Buku
                        </button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</x-app-layout>
