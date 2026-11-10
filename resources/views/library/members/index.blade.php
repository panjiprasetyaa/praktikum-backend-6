<x-app-layout>
    <x-slot name="header">
        <div class="flex flex-wrap justify-between items-center gap-3">
            <div>
                <h2 class="font-semibold text-xl text-gray-800 leading-tight">
                    {{ __('Manajemen Anggota Perpustakaan (Membership Context)') }}
                </h2>
                <p class="text-xs text-gray-500 mt-1">
                    Eager Loading <code>Member::with('roles')</code> aktif — Total SQL dieksekusi: <span class="font-bold text-gray-800">{{ $queryCount }} Query</span>
                </p>
            </div>
            @if(Auth::user()->role === 'admin')
                <a href="{{ route('library.members.trash') }}" class="bg-gray-600 hover:bg-gray-800 text-white text-sm font-semibold py-2 px-4 rounded">
                    Trash / Restore (Admin)
                </a>
            @endif
        </div>
    </x-slot>

    <div class="py-8">
        <div class="max-w-7xl mx-auto sm:px-6 lg:px-8 space-y-6">
            @if (session('success'))
                <div class="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded">
                    {{ session('success') }}
                </div>
            @endif

            {{-- Form Tambah Anggota Cepat --}}
            <div class="bg-white shadow-sm sm:rounded-lg p-6">
                <h3 class="font-semibold text-gray-800 mb-3 text-sm">Daftarkan Anggota Baru</h3>
                <form method="POST" action="{{ route('library.members.store') }}" class="grid grid-cols-1 md:grid-cols-5 gap-3 items-end">
                    @csrf
                    <div>
                        <label class="block text-xs font-medium text-gray-700">Nama Lengkap</label>
                        <input type="text" name="name" required class="mt-1 w-full rounded-md border-gray-300 shadow-sm text-sm">
                    </div>
                    <div>
                        <label class="block text-xs font-medium text-gray-700">Email</label>
                        <input type="email" name="email" required class="mt-1 w-full rounded-md border-gray-300 shadow-sm text-sm">
                    </div>
                    <div>
                        <label class="block text-xs font-medium text-gray-700">Status</label>
                        <select name="status" class="mt-1 w-full rounded-md border-gray-300 shadow-sm text-sm">
                            <option value="active">Active (Boleh Pinjam)</option>
                            <option value="suspended">Suspended (Dilarang Pinjam)</option>
                        </select>
                    </div>
                    <div>
                        <label class="block text-xs font-medium text-gray-700">Role</label>
                        <select name="role_id" class="mt-1 w-full rounded-md border-gray-300 shadow-sm text-sm">
                            @foreach($roles as $role)
                                <option value="{{ $role->id }}">{{ $role->name }}</option>
                            @endforeach
                        </select>
                    </div>
                    <div>
                        <button type="submit" class="w-full bg-blue-600 hover:bg-blue-800 text-white text-sm font-semibold py-2 px-4 rounded">
                            + Tambah Anggota
                        </button>
                    </div>
                </form>
            </div>

            {{-- Tabel Daftar Anggota --}}
            <div class="bg-white overflow-hidden shadow-sm sm:rounded-lg p-6 overflow-x-auto">
                <table class="min-w-full border border-gray-200 text-sm">
                    <thead>
                        <tr class="bg-gray-100 text-gray-700 uppercase text-xs">
                            <th class="py-3 px-4 text-left border-b">Kode Anggota</th>
                            <th class="py-3 px-4 text-left border-b">Nama & Email</th>
                            <th class="py-3 px-4 text-left border-b">Role</th>
                            <th class="py-3 px-4 text-center border-b">Status</th>
                            <th class="py-3 px-4 text-center border-b">Aksi</th>
                        </tr>
                    </thead>
                    <tbody class="divide-y divide-gray-200">
                        @forelse ($members as $member)
                            <tr class="hover:bg-gray-50">
                                <td class="py-3 px-4 font-mono text-xs">{{ $member->member_code }}</td>
                                <td class="py-3 px-4">
                                    <div class="font-semibold">{{ $member->name }}</div>
                                    <div class="text-xs text-gray-500">{{ $member->email }}</div>
                                </td>
                                <td class="py-3 px-4 text-xs">
                                    {{ $member->roles->pluck('name')->join(', ') ?: '-' }}
                                </td>
                                <td class="py-3 px-4 text-center">
                                    @if($member->status === 'active')
                                        <span class="bg-green-100 text-green-800 font-bold px-2.5 py-0.5 rounded text-xs">Active</span>
                                    @else
                                        <span class="bg-red-100 text-red-800 font-bold px-2.5 py-0.5 rounded text-xs">Suspended</span>
                                    @endif
                                </td>
                                <td class="py-3 px-4 text-center">
                                    <form action="{{ route('library.members.destroy', $member->id) }}" method="POST"
                                        onsubmit="return confirm('Soft delete anggota ini?');">
                                        @csrf
                                        @method('DELETE')
                                        <button type="submit" class="text-red-600 hover:text-red-800 font-semibold text-xs">Soft Delete</button>
                                    </form>
                                </td>
                            </tr>
                        @empty
                            <tr><td colspan="5" class="py-4 text-center text-gray-500">Belum ada anggota terdaftar.</td></tr>
                        @endforelse
                    </tbody>
                </table>
                <div class="mt-4">{{ $members->links() }}</div>
            </div>
        </div>
    </div>
</x-app-layout>
