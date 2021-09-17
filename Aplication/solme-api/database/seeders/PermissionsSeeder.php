<?php
/*Run php artisan migrate:fresh --seed --seeder=PermissionsSeeder*/
namespace Database\Seeders;

use Illuminate\Database\Seeder;
use Spatie\Permission\Models\Permission;
use Spatie\Permission\Models\Role;
use Spatie\Permission\PermissionRegistrar;

class PermissionsSeeder extends Seeder
{
    /**
     * Run the database seeds.
     *
     * @return void
     */
    public function run()
    {
        // Reset cached roles and permissions
        app()[PermissionRegistrar::class]->forgetCachedPermissions();

        $permissions = [
            "Create User",
            "Delete User",
            "Create Role",
            "View All Users",
            "Edit All Users",
            "Assign Role",
            "Unassign Role",
            "View All Permissions",
            "View All Roles",
            "Listar Tableros",
            "Crear Tablero",
            "Ver Usuario Tablero",
            "Listar usuarios",
            "Editar Tablero",
            "Tablero usuario",
            "Play tablero",
            "Verificar Usuarios",
            "Resultado",
            "Listar metricas"
        ];

        $adminRole = Role::updateOrCreate(['name' => 'admin', 'guard_name' => 'api']);

        // create permissions
        foreach ($permissions as $perm_name) {
            $permission = Permission::updateOrCreate(['name' => $perm_name,
                'guard_name' => 'api']);

            $adminRole->givePermissionTo($perm_name);
        }

        // Se crea el rol de jugador
        $roleUser = Role::updateOrCreate(['name' => 'jugador', 'guard_name' => 'api']);
        $roleUser->givePermissionTo('View All Users');
        $roleUser->givePermissionTo('Tablero usuario');
        $roleUser->givePermissionTo('Play tablero');
        $roleUser->givePermissionTo('Resultado');
        $roleUser->givePermissionTo('Listar metricas');

        // Se crea el rol de entrenador
        $roleUser = Role::updateOrCreate(['name' => 'entrenador', 'guard_name' => 'api']);
        $roleUser->givePermissionTo('View All Users');

    }
}
