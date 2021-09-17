<?php

namespace Database\Seeders;

use Illuminate\Database\Seeder;
use \App\Models\User;
use \App\Models\Product;
use \Spatie\Permission\Models\Role;

/* Refrescar seed */
/* php artisan migrate:fresh --seed */

class DatabaseSeeder extends Seeder
{
    /**
     * Seed the application's database.
     *
     * @return void
     */
    public function run()
    {
        // \App\Models\User::factory(10)->create();
        $this->call([
            PermissionsSeeder::class,
        ]);

        $user = new User([
            'name' => 'Admin',
            'last_name' => 'Total',
            'email' => 'admin@gmail.com',
            'phone_number' => '3215465154',
            'address' => 'Calle 5 #7-04',
            'born_date' => '12/06/1999',
            'basic_profile' => 'Futbol',
            'password' => bcrypt('1234'),
            'role' => 'admin'
        ]);
        $user->save();
        $role = Role::where('name', 'admin')->first();
        $user->assignRole($role);

        $user2 = new User([
            'name' => 'Jugador',
            'last_name' => 'Prueba',
            'email' => 'jugador@gmail.com',
            'phone_number' => '3215465154',
            'address' => 'Calle 5 #7-04',
            'born_date' => '12/06/1999',
            'basic_profile' => 'Futbol',
            'password' => bcrypt('1234'),
            'role' => 'jugador'
        ]);
        $user2->save();
        $role = Role::where('name', 'jugador')->first();
        $user2->assignRole($role);

        $user3 = new User([
            'name' => 'Entrenador',
            'last_name' => 'Prueba',
            'email' => 'entrenador@gmail.com',
            'phone_number' => '3215465154',
            'address' => 'Calle 5 #7-04',
            'born_date' => '12/06/1999',
            'basic_profile' => 'Futbol',
            'password' => bcrypt('1234'),
            'role' => 'entrenador'
        ]);
        $user3->save();
        $role = Role::where('name', 'entrenador')->first();
        $user3->assignRole($role);


        $product = new Product([
            'device_type'=>'Tablero',
            'device_name'=>'Prueba',
            'device_description'=>'Tablero de prueba inicial',
            'device_code' => 'A1B2'
        ]);
        $product->save();
        
    }
}
