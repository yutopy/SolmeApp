<?php

namespace App\Http\Controllers;

use App\Models\ShoppingCar;
use App\Models\User;
use Illuminate\Http\Request;
use Illuminate\Http\Response;

class ShoppingCarController extends Controller
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

    public function anotacionFracaso(Request $request){
        $resultado = new ShoppingCar;
        $resultado->user_id = $request->user_id;
        $resultado->device_id = $request->device_id;
        $resultado->resultado = $request->resultado;
        $resultado->deporte = $request->deporte;
        $resultado->save();
        return response()->json($resultado)->setStatusCode(Response::HTTP_OK);
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
        //
    }

    /**
     * Display the specified resource.
     *
     * @param  \App\Models\ShoppingCar  $shoppingCar
     * @return \Illuminate\Http\Response
     */
    public function listarMetricas(Request $request)
    {
        $cant_todos_datos = ShoppingCar::where("user_id","=",$request->user_id)->count();
        $count_todos_aciertos = ShoppingCar::where("user_id","=",$request->user_id,'and')
                                            ->where("resultado","=","Anotacion")->count();
        $count_todos_fracasos = ShoppingCar::where("user_id","=",$request->user_id,'and')
                                            ->where("resultado","=","Fracaso")->count();


        $metrica1=[
            'titulo' => 'Todos los datos',
            'aciertos' => $count_todos_aciertos,
            'fracasos' => $count_todos_fracasos,
            'cant_datos' => $cant_todos_datos
        ];

        return response()->json([$metrica1])->setStatusCode(Response::HTTP_OK);

    }

    /**
     * Show the form for editing the specified resource.
     *
     * @param  \App\Models\ShoppingCar  $shoppingCar
     * @return \Illuminate\Http\Response
     */
    public function edit(ShoppingCar $shoppingCar)
    {
        //
    }

    /**
     * Update the specified resource in storage.
     *
     * @param  \Illuminate\Http\Request  $request
     * @param  \App\Models\ShoppingCar  $shoppingCar
     * @return \Illuminate\Http\Response
     */
    public function update(Request $request, ShoppingCar $shoppingCar)
    {
        //
    }

    /**
     * Remove the specified resource from storage.
     *
     * @param  \App\Models\ShoppingCar  $shoppingCar
     * @return \Illuminate\Http\Response
     */
    public function destroy(ShoppingCar $shoppingCar)
    {
        //
    }
}
