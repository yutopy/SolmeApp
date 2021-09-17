<?php

namespace App\Http\Controllers;

use App\Models\Product;
use App\Models\User;
use Illuminate\Http\Request;
use Illuminate\Http\Response;

class ProductController extends Controller
{
    /**
     * Display a listing of the resource.
     *
     * @return \Illuminate\Http\Response
     */
    public function index()
    {
        //
    }

    /**
     * Show the form for creating a new resource.
     *
     * @return \Illuminate\Http\Response
     */
    public function create()
    {
        //
    }

    /**
     * Store a newly created resource in storage.
     *
     * @param  \Illuminate\Http\Request  $request
     * @return \Illuminate\Http\Response
     */
    public function store(Request $request)
    {
        $image = $request->file('product_photo');
        $image->move('public/img', $image->getClientOriginalName());
        // $nombre_tabla->imagen = image->getClientOriginalName();

        $product = new Product;
        $product->product_type = $request->product_type;
        $product->product_name = $request->product_name;
        $product->product_description = $request->product_description;
        $product->product_price = intval($request->product_price);
        $product->product_photo = $image->getClientOriginalName();

        $product->save();

        return response()->json(['product' => $product])->setStatusCode(Response::HTTP_OK);
    }

    /**
     * Display the specified resource.
     *
     * @param  \App\Models\Product  $product
     * @return \Illuminate\Http\Response
     */
    public function show(Product $product)
    {
        //
    }

    public function listarTableros(Product $product)
    {
        $tableros = Product::all();
        return response()->json($tableros)->setStatusCode(Response::HTTP_OK);
    }

    public function crearTablero(Request $request){
        $tablero = new Product;
        $tablero->device_type = $request->device_type;
        $tablero->device_name = $request->device_name;
        $tablero->device_description = $request->device_description;
        $tablero->device_code = $request->device_code;
        $tablero->save();
        return response()->json($tablero)->setStatusCode(Response::HTTP_OK);
    }

    public function usuarioTablero(Request $request){
        $user = User::where('id', '=', $request->user_id)->first();
        return response()->json($user)->setStatusCode(Response::HTTP_OK);
    }

    public function editarTablero(Request $request){
        $tablero = Product::where('id', '=', intval($request->tablero_id))->first();
        $tablero->device_type = $request->new_type;
        $tablero->device_name = $request->new_name;
        $tablero->device_description = $request->new_description;
        $tablero->device_code = $request->new_code;
        $tablero->user_id = $request->new_user;
        $tablero->status = $request->new_status;
        $tablero->save();
        return response()->json($tablero)->setStatusCode(Response::HTTP_OK);
    }

    /**
     * Show the form for editing the specified resource.
     *
     * @param  \App\Models\Product  $product
     * @return \Illuminate\Http\Response
     */
    public function edit(Product $product) 
    {
        //
    }

    /**
     * Update the specified resource in storage.
     *
     * @param  \Illuminate\Http\Request  $request
     * @param  \App\Models\Product  $product
     * @return \Illuminate\Http\Response
     */
    public function update(Request $request, Product $product)
    {
        //
    }

    /**
     * Remove the specified resource from storage.
     *
     * @param  \App\Models\Product  $product
     * @return \Illuminate\Http\Response
     */
    public function destroy(Product $product)
    {
        //
    }

    public function listarTableroUsuario(Request $request)
    {
        $tablero = Product::where("user_id", "=", $request->user_id)->first();
        return response()->json([$tablero])->setStatusCode(Response::HTTP_OK);
    }

    public function playTablero(Request $request)
    {
        $tablero = Product::where("id", "=", $request->tablero_id)->first();
        $tablero->status="Encendido";
        $tablero->save();
        return response()->json([$tablero])->setStatusCode(Response::HTTP_OK);
    }

    public function offTablero(Request $request)
    {
        $tablero = Product::where("id", "=", $request->tablero_id)->first();
        $tablero->status="Apagado";
        $tablero->save();
        return response()->json([$tablero])->setStatusCode(Response::HTTP_OK);
    }



    public function estadoTablero(Request $request){
        $tablero = Product::where("device_code","=",$request->device_code)->first();
        return response()->json($tablero)->setStatusCode(Response::HTTP_OK);
    }

    public function actualizarEstado(Request $request){
        $tablero = Product::where("device_code","=",$request->device_code)->first();
        $tablero->status = $request->status;
        $tablero->save();
        return response()->json($tablero)->setStatusCode(Response::HTTP_OK);
    }

}
