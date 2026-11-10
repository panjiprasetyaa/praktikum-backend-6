<?php

namespace Modules\Membership\Controllers;

use App\Http\Controllers\Controller;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\DB;
use Modules\Membership\Models\Member;
use Modules\Membership\Models\Role;

class MemberController extends Controller
{
    /**
     * Menampilkan daftar anggota perpustakaan dengan Eager Loading roles.
     */
    public function index()
    {
        DB::flushQueryLog();
        DB::enableQueryLog();

        $members = Member::with('roles')->latest()->paginate(10);
        $roles = Role::all();
        $queryCount = count(DB::getQueryLog());

        return view('library.members.index', compact('members', 'roles', 'queryCount'));
    }

    /**
     * Mendaftarkan anggota baru.
     */
    public function store(Request $request)
    {
        $validated = $request->validate([
            'name' => ['required', 'string', 'max:255'],
            'email' => ['required', 'email', 'unique:members,email'],
            'phone' => ['nullable', 'string', 'max:30'],
            'status' => ['required', 'in:active,suspended'],
            'role_id' => ['nullable', 'exists:roles,id'],
        ]);

        $member = Member::create([
            'member_code' => 'MBR-' . date('Y') . '-' . rand(100, 999),
            'name' => $validated['name'],
            'email' => $validated['email'],
            'phone' => $validated['phone'] ?? null,
            'status' => $validated['status'],
            'max_loans' => 3,
        ]);

        if (!empty($validated['role_id'])) {
            $member->roles()->sync([$validated['role_id']]);
        }

        return redirect()->route('library.members.index')
            ->with('success', "Anggota '{$member->name}' ({$member->member_code}) berhasil didaftarkan.");
    }

    /**
     * Soft delete anggota.
     */
    public function destroy(Member $member)
    {
        $name = $member->name;
        $member->delete();

        return redirect()->route('library.members.index')
            ->with('success', "Anggota '{$name}' dipindahkan ke Trash (Soft Delete).");
    }

    /**
     * Menampilkan daftar anggota terhapus khusus Admin.
     */
    public function trash()
    {
        $trashedMembers = Member::onlyTrashed()->with('roles')->latest('deleted_at')->paginate(10);
        return view('library.members.trash', compact('trashedMembers'));
    }

    /**
     * Mengembalikan anggota terhapus (Restore oleh Admin).
     */
    public function restore(int $id)
    {
        $member = Member::onlyTrashed()->findOrFail($id);
        $member->restore();

        return redirect()->route('library.members.trash')
            ->with('success', "Anggota '{$member->name}' berhasil di-restore oleh Admin.");
    }
}
