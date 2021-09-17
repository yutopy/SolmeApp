<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use App\Models\User;
use Spatie\Permission\Models\Role;
use Spatie\Permission\Models\Permission;
use Illuminate\Support\Facades\Log;
use Illuminate\Support\Facades\Auth;
use Validator;
use Illuminate\Http\Response;

class RoleManager extends Controller
{
    public function permissionsIndex()
    {
        error_log('Admin '.Auth::user()->hasRole('admin'));
        return Permission::all();
    }


    public function rolesIndex()
    {
        return Role::all();
    }

    public function rolesStore(Request $request){
        $validator = Validator::make($request->all(), [
            'name' => 'required',
        ]);
        if ($validator->fails()) {
            return response()->json(['error'=>$validator->errors()])->setStatusCode(Response::HTTP_UNPROCESSABLE_ENTITY); // 422
        }
        $role = Role::updateOrCreate(['name' => $request->name, 'guard_name' => 'api']);

        return response()->json(['role' => $role])->setStatusCode(Response::HTTP_CREATED); // 201
    }

    public function rolesAddUser(Request $request, Role $role, User $user)
    {

        $user->assignRole($role);

        return response()->json([
            "message" => $role->name . " Role successfully assigned to User!"
        ], 200);
    }

    public function rolesRemoveUser(Request $request, Role $role, User $user)
    {
        $user->removeRole($role);

        return response()->json([
            "message" => $role->name . " Role successfully removed from User"
        ], 200);
    }
}
