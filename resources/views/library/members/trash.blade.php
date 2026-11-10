<x-app-layout>
    <x-slot name="header">
        <div class="flex justify-between items-center">
            <h2 class="font-semibold text-xl text-gray-800 leading-tight">
                {{ __('Trash & Restore Anggota (Khusus Admin)') }}
            </h2>
            <a href="{{ route('library.members.index') }}" class="text-sm text-gray-600 hover:text-gray-900">
                &larr; Kembali ke Daftar Anggota
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
                            <th class="py-3 px-4 text-left border-b">Kode</th>
                            <th class="py-3 px-4 text-left border-b">Nama & Email</th>
                            <th class="py-3 px-4 text-left border-b">Dihapus Pada</th>
                            <th class="py-3 px-4 text-center border-b">Aksi Admin</th>
                        </tr>
                    </thead>
                    <tbody class="divide-y divide-gray-200">
                        @forelse ($trashedMembers as $member)
                            <tr>
                                <td class="py-3 px-4 font-mono text-xs">{{ $member->member_code }}</td>
                                <td class="py-3 px-4">
                                    <div class="font-semibold">{{ $member->name }}</div>
                                    <div class="text-xs text-gray-500">{{ $member->email }}</div>
                                </td>
                                <td class="py-3 px-4 text-xs text-gray-500">{{ $member->deleted_at }}</td>
                                <td class="py-3 px-4 text-center">
                                    <form action="{{ route('library.members.restore', $member->id) }}" method="POST">
                                        @csrf
                                        <button type="submit" class="bg-green-600 hover:bg-green-800 text-white font-semibold py-1 px-3 rounded text-xs">
                                            Restore Data
                                        </button>
                                    </form>
                                </td>
                            </tr>
                        @empty
                            <tr>
                                <td colspan="4" class="py-6 text-center text-gray-500">Trash anggota kosong.</td>
                            </tr>
                        @endforelse
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</x-app-layout>
