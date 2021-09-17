<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;
use Carbon\Carbon;
use App\Models\User;
use Spatie\Permission\Models\Permission;
use \Spatie\Permission\Models\Role;
use App\Http\Requests\Signup as SignUpRequest;
use App\Http\Resources\Signup as SignUpResource;

use App\Http\Requests\Login as LoginRequest;


class AuthController extends Controller
{
    /**
     * Create user
     *
     * @param  [string] name
     * @param  [string] email
     * @param  [string] password
     * @param  [string] password_confirmation
     * @return [string] message
     */
    public function signup(SignUpRequest $request)
    {
        /*
        $user = new User([
            'name' => $request->name,
            'email' => $request->email,
            'password' => bcrypt($request->password),
            'cc' => intval($request->cc),
            'last_name_1' => $request->last_name_1,
            'last_name_2' => $request->last_name_2,
            'phone_number' => $request->phone_number,
            'city' => $request->city
        ]);
        */

        $user = new User;
        $user->name = $request->name;
        $user->last_name = $request->last_name;
        $user->email = $request->email;
        $user->phone_number = $request->phone_number;
        $user->address = $request->address;
        $user->born_date = $request->born_date;
        $user->basic_profile = $request->basic_profile;
        $user->password = bcrypt($request->password);
        $user->role = $request->role;
        $user->save();

        $role = Role::where('name', $user->role)->first();
        $user->assignRole($role);

        return response()->json(new SignUpResource($user), 201);
    }

    /**
     * Login user and create token
     *
     * @param  [string] email
     * @param  [string] password
     * @param  [boolean] remember_me
     * @return [string] access_token
     * @return [string] token_type
     * @return [string] expires_at
     */
    public function login(LoginRequest $request)
    {

        $credentials = request(['email', 'password']);
        //print_r($credentials);

        if (!Auth::attempt($credentials))
            return response()->json([
                'message' => 'Unauthorized'
            ], 401);

        $user = $request->user();
        $tokenResult = $user->createToken($user->email . '-' . now());
        $token = $tokenResult->token;

        $token->save();

        return response()->json([
            'access_token' => $tokenResult->accessToken,
            'token_type' => 'Bearer',
            'id' => $user->id,
            'role' => $user->role,
            'expires_at' => Carbon::parse(
                $tokenResult->token->expires_at
            )->toDateTimeString()
        ], 201);
    }

    /**
     * Logout user (Revoke the token)
     *
     * @return [string] message
     */
    public function logout(Request $request)
    {
        $request->user()->token()->revoke();
        return response()->json([
            'message' => 'Successfully logged out'
        ]);
    }

    /**
     * Get the authenticated User
     *
     * @return [json] user object
     */
    public function user(Request $request)
    {
        return response()->json([
            'user' => $request->user(),
            'permissions' => Auth::user()->getPermissionsViaRoles(),
            'roles' => Auth::user()->getRoleNames(),
            'isAdmin' => Auth::user()->hasRole('admin'),
            //  'adminRoleUser' => User::with('roles')->get(),
            //  'permission' => Permission::all()
        ]);
    }
}
