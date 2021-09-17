<?php

use Illuminate\Http\Request;
use App\Http\Controllers\AuthController;
use App\Http\Controllers\RoleManager;
use App\Http\Controllers\UserController;
use App\Http\Controllers\ProductController;
use App\Http\Controllers\ShoppingCarController;


/*
|--------------------------------------------------------------------------
| API Routes
|--------------------------------------------------------------------------
|
| Here is where you can register API routes for your application. These
| routes are loaded by the RouteServiceProvider within a group which
| is assigned the "api" middleware group. Enjoy building your API!
|
*/

Route::post('estado-tablero', [ProductController::class, 'estadoTablero']);
Route::post('actualizar-estado', [ProductController::class, 'actualizarEstado']);

Route::group(['prefix' => 'auth', 'middleware' => 'cors'], function () {
    Route::post('login', [AuthController::class, 'login']);
    Route::post('signup', [AuthController::class, 'signup']);
    Route::post('estado-tablero', [ProductController::class, 'estadoTablero']);
    Route::post('actualizar-estado', [ProductController::class, 'actualizarEstado']);

    Route::group(['middleware' => 'auth:api'], function () {
        Route::get('logout', [AuthController::class, 'logout']);
        Route::get('user', [AuthController::class, 'user']);
        //Route::post('signup', [AuthController::class, 'signup'])->middleware(['role:admin']);
    });
});

Route::group(['middleware' => 'auth:api'], function () {
    // Users end-points
    Route::get('/user', [UserController::class, 'index'])
        ->middleware(['permission:View All Users']);
    Route::get('/user/{user}', [UserController::class, 'show'])
        ->middleware(['permission:View All Users']);
    Route::post('/user', [UserController::class, 'store'])
        ->middleware(['permission:Create User']);
    Route::put('/user/{user}', [UserController::class, 'update'])
        ->middleware(['permission:Edit All Users']);
    Route::delete('/user/{user}', [UserController::class, 'destroy'])
        ->middleware(['permission:Delete User']);

    // Roles and permissions end-points
    Route::get('/permissions', [RoleManager::class, 'permissionsIndex'])
        ->middleware(['permission:View All Permissions']);
    Route::get('/roles', [RoleManager::class, 'rolesIndex'])
        ->middleware('permission:View All Roles');
    Route::post('/roles', [RoleManager::class, 'rolesStore'])
        ->middleware('permission:Create Role');
    Route::post('/roles/{role}/assign/{user}', [RoleManager::class, 'rolesAddUser'])
        ->middleware('permission:Assign Role');
    Route::post('/roles/{role}/unassign/{user}', [RoleManager::class, 'rolesRemoveUser'])
        ->middleware('permission:Unassign Role');


    //end-point rol jugador
    Route::post('/listar-tablero-usuario',[ProductController::class, 'listarTableroUsuario'])
        ->middleware(['permission:Tablero usuario']);

    Route::post('/play-tablero',[ProductController::class, 'playTablero'])
        ->middleware(['permission:Play tablero']);

    Route::post('/off-tablero',[ProductController::class, 'offTablero'])
        ->middleware(['permission:Play tablero']);

    
    Route::post('/anotacion-fracaso',[ShoppingCarController::class, 'anotacionFracaso'])
        ->middleware(['permission:Resultado']);

    Route::post('/listar-metricas',[ShoppingCarController::class, 'listarMetricas'])
        ->middleware(['permission:Listar metricas']);



    
    // end-points administrador

        //Tableros

    Route::get('/listar-usuarios', [UserController::class, 'listarUsuarios'])
        ->middleware(['permission:Listar usuarios']);

    Route::get('/listar-tableros', [ProductController::class, 'listarTableros'])
        ->middleware(['permission:Listar Tableros']);
    
    Route::post('/usuario-tablero', [ProductController::class, 'usuarioTablero'])
        ->middleware(['permission:Ver Usuario Tablero']);

    Route::post('/editar-tablero', [ProductController::class, 'editarTablero'])
        ->middleware(['permission:Editar Tablero']);

    Route::post('/crear-tablero', [ProductController::class, 'crearTablero'])
        ->middleware(['permission:Crear Tablero']);

    Route::post('/create-product-admin', [ProductController::class, 'store'])
        ->middleware(['permission:Subir archivo PE04']);

    Route::get('/validar-usuarios', [UserController::class, 'validarUsuarios'])
        ->middleware(['permission:Verificar Usuarios']);

    Route::get('/verificar-usuarios', [UserController::class, 'verificarUsuarios'])
        ->middleware(['permission:Verificar Usuarios']);

    Route::post('/rechazar-usuario', [UserController::class, 'rechazarUsuario'])
        ->middleware(['permission:Verificar Usuarios']);

    Route::post('/aceptar-usuario', [UserController::class, 'aceptarUsuario'])
        ->middleware(['permission:Verificar Usuarios']);

        //Validar solicitudes


    Route::get('/cargar-solicitudes', [FichaIngresoController::class, 'cargarSolicitudes'])
        ->middleware(['permission:Subir archivo PE04']);

    Route::post('/rechazar-solicitud', [FichaIngresoController::class, 'rechazarSolicitud'])
        ->middleware(['permission:Subir archivo PE04']);

    Route::post('/aceptar-solicitud', [FichaIngresoController::class, 'aceptarSolicitud'])
        ->middleware(['permission:Subir archivo PE04']);

    //Route::post('/ajustar-valores', [ReadingController::class, 'ajustesMoto'])
    //->middleware(['permission:Subir archivo PE04']);

                
/*
    Route::get('/pe04/centro/{centro}/titulada', [Pe04Controller::class, 'obtenerTitulada'])
        ->middleware(['permission:Analisis PE04']);
    Route::get('/pe04/centro/{centro}/complementaria', [Pe04Controller::class, 'obtenerComplementaria'])
        ->middleware(['permission:Analisis PE04']);

        //Listar las fichas activas. Recibe el código del centro
    Route::get('/pe04/fichas-activas/{codigo_centro}', [Pe04Controller::class, 'listarFichasActivas'])
    ->middleware(['permission:Ver fichas activas']);

    // Registro Calificado
    Route::post('/registro-calificado/import', [RegistroCalificadoController::class, 'import'])
        ->middleware(['permission:Cargar registro calificado']);

    // Aprobar programa indicativa
    
        // Cargar acta regional indicativa (incluye aprobacion regional)
    Route::put('/programacion-indicativa/cargar-acta', [CatalogoIndicativaController::class, 'anexarActa'])
        ->middleware(['permission:Anexar acta']);

        // Aprobacion centro
    Route::put('/programacion-indicativa/aprobar-centro', [CatalogoIndicativaController::class, 'aprobarCentro'])
        ->middleware(['permission:Aprobar programa indicativa']);

        // Aprobacion nacional
    Route::put('/programacion-indicativa/aprobar-nacional', [CatalogoIndicativaController::class, 'aprobarNacional'])
    ->middleware(['permission:Aprobar programa indicativa']);

        // Rechazar Regional
    Route::put('/programacion-indicativa/rechazar-regional', [CatalogoIndicativaController::class, 'rechazarRegional'])
    ->middleware(['permission:Aprobar programa indicativa']);

        // Rechazar Nacional
    Route::put('/programacion-indicativa/rechazar-nacional', [CatalogoIndicativaController::class, 'rechazarNacional'])
    ->middleware(['permission:Aprobar programa indicativa']);

    */
});
