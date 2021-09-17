<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Http\Response;
use Validator;
use \App\Models\User;

class UserController extends Controller
{

    /**
     * Display a listing of the resource.
     *
     * @return \Illuminate\Http\Response
     */
    public function index()
    {
        $users = User::all();
        return response()->json(['users' => $users])->setStatusCode(Response::HTTP_OK); // 200
    }

    public function listarUsuarios()
    {
        $users = User::all();
        return response()->json($users)->setStatusCode(Response::HTTP_OK); // 200
    }

    public function validarUsuarios()
    {
        //$users_cuidadora = User::where('estado','=','0', 'and')->where('role','=','cuidadora')->get();
        $count_cuidadora = User::where('estado','=','0', 'and')->where('role','=','cuidadora')->count();

        //$users_doctor = User::where('estado','=','0', 'and')->where('role','=','doctor')->get();
        $count_doctor = User::where('estado','=','0', 'and')->where('role','=','doctor')->count();

        //$users_enfermera = User::where('estado','=','0', 'and')->where('role','=','enfermera')->get();
        $count_enfermera = User::where('estado','=','0', 'and')->where('role','=','enfermera')->count();

        //$users_auxiliar = User::where('estado','=','0', 'and')->where('role','=','auxiliarEnfermeria')->get();
        $count_auxiliar = User::where('estado','=','0', 'and')->where('role','=','auxiliarEnfermeria')->count();

        //$users_vigilancia = User::where('estado','=','0', 'and')->where('role','=','vigilancia')->get();
        $count_vigilancia = User::where('estado','=','0', 'and')->where('role','=','vigilancia')->count();

        //$users_acudiente = User::where('estado','=','0', 'and')->where('role','=','acudiente')->get();
        $count_acudiente = User::where('estado','=','0', 'and')->where('role','=','acudiente')->count();

        //$users_adulto = User::where('estado','=','0', 'and')->where('role','=','adultoMayor')->get();
        $count_adulto = User::where('estado','=','0', 'and')->where('role','=','adultoMayor')->count();


        return response()->json(['count_cuidadora' => $count_cuidadora,
        'count_doctor' => $count_doctor,
        'count_enfermera' => $count_enfermera,
        'count_auxiliar' => $count_auxiliar,
        'count_vigilancia' => $count_vigilancia,
        'count_acudiente' => $count_acudiente,
        'count_adulto' => $count_adulto])->setStatusCode(Response::HTTP_OK); // 200
    }

    public function verificarUsuarios(Request $request)
    {
        $users_aproved = User::where('estado','=','1', 'and')->where('role','=',$request->role)->get();
        $users_rejected = User::where('estado','=','2', 'and')->where('role','=',$request->role)->get();
        $users_waiting = User::where('estado','=','0', 'and')->where('role','=',$request->role)->get();

        return response()->json(['users_aproved'=>$users_aproved, 'users_rejected'=>$users_rejected, 'users_waiting'=>$users_waiting])->setStatusCode(Response::HTTP_OK); // 200
    }

    public function aceptarUsuario(Request $request)
    {
        $user = User::where('id','=',$request->user_id)->first();
        $user->estado = 1;
        
        if ($user->save()){
            return response()->json($user)->setStatusCode(Response::HTTP_OK); // 200
        }

    }

    public function rechazarUsuario(Request $request)
    {
        $user = User::where('id','=',$request->user_id)->first();
        $user->estado = 2;
        
        if($user->save()){
            return response()->json($user)->setStatusCode(Response::HTTP_OK); // 200
        }

    }

    /**
     * Store a newly created resource in storage.
     *
     * @param  \Illuminate\Http\Request  $request
     * @return \Illuminate\Http\Response
     */
    public function store(Request $request)
    {
        //Validating title and body field
        $validator = Validator::make($request->all(), [
            'name' => 'required|string',
            'last_name' => 'required|string',
            'email' => 'required|string|email',
            'phone_number' => 'required|string',
            'address' => 'required|string',
            'born_date' => 'required|string',
            'basic_profile' => 'required|string',
            'password' => 'required|string',
            'role' => 'required|string',
        ]);
        if ($validator->fails()) {
            return response()->json(['error'=>$validator->errors()])->setStatusCode(Response::HTTP_UNPROCESSABLE_ENTITY); // 422
        }

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

        if($user->save()){
            return response()->json(['user' => $user])->setStatusCode(Response::HTTP_CREATED); // 201
        }
        return response()->json(['error' => "Unable to create"])->setStatusCode(Response::HTTP_INTERNAL_SERVER_ERROR);        // 500
    }

    /**
     * Display the specified resource.
     *
     * @param  \App\User  $user
     * @return \Illuminate\Http\Response
     */
    public function show(User $user)
    {
        return response()->json(['user'=>$user])->setStatusCode(Response::HTTP_OK); // 200
    }

    /**
     * Update the specified resource in storage.
     *
     * @param  \Illuminate\Http\Request  $request
     * @param  \App\User  $user
     * @return \Illuminate\Http\Response
     */
    public function update(Request $request, User $user)
    {
        $validator = Validator::make($request->all(), [
            'name' => 'required',
            'email' => 'required|email',
        ]);
        if ($validator->fails()) {
            return response()->json(['error'=>$validator->errors()])->setStatusCode(Response::HTTP_UNPROCESSABLE_ENTITY); // 422
        }
        $input = $request->all();
        $user->name = $input['name'];
        $user->email = $input['email'];
        if($user->save()){
            return response()->json(['user' => $user])->setStatusCode(Response::HTTP_OK); // 200
        }
        return response()->json(['error' => "Unable to create"])->setStatusCode(Response::HTTP_NOT_MODIFIED);        // 304
    }

    /**
     * Remove the specified resource from storage.
     *
     * @param  \App\User  $user
     * @return \Illuminate\Http\Response
     */
    public function destroy(User $user)
    {
        $user->delete();
        return response()->json(null)->setStatusCode(Response::HTTP_NO_CONTENT);        // 204
    }

    public function newUser(Request $request)
    {
        //Validating title and body field
        $validator = Validator::make($request->all(), [
            'name' => 'required|string',
            'email' => 'required|string|email',
            'password' => 'required|string',
            'identification' => 'required',
            'last_name' => 'required|string',
            'phone_number' => 'required|string',
            'address' => 'required|string',
            'id_date' => 'required|string',
            'basic_profile' => 'required|string',
            'role' => 'required|string',
            'born_date' => 'required|string',
        ]);
        if ($validator->fails()) {
            return response()->json(['error'=>$validator->errors()])->setStatusCode(Response::HTTP_UNPROCESSABLE_ENTITY); // 422
        }
        $user = new User;
        $user->name = $request->name;
        $user->email = $request->email;
        $user->password = bcrypt($request->password);
        $user->identification = intval($request->identification);
        $user->last_name = $request->last_name;
        $user->phone_number = $request->phone_number;
        $user->address = $request->address;
        $user->id_date = $request->id_date;
        $user->role = $request->role;
        $user->born_date = $request->born_date;
        $user->id_medico = $request->id_medico;
        $user->institution_name = $request->institution_name;
        $user->id_old_man = intval($request->id_old_man);
        $user->profession = $request->profession;
        $user->relationship = $request->relationship;
        $user->tipo_cuidadora = $request->tipo_cuidadora;
        $user->basic_profile = $request->basic_profile;

        if($user->save()){
            return response()->json(['user' => $user])->setStatusCode(Response::HTTP_CREATED); // 201
        }
        return response()->json(['error' => "Unable to create"])->setStatusCode(Response::HTTP_INTERNAL_SERVER_ERROR);        // 500
    }

}
