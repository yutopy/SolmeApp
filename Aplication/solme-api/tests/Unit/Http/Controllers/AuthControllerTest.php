<?php

namespace Tests\Unit\Http\Controllers;

use App\Models\User;
use Spatie\Permission\Models\Role;
use Spatie\Permission\Models\Permission;
use Illuminate\Foundation\Testing\WithFaker;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Tests\TestCase;
use Illuminate\Contracts\Auth\Authenticatable;

class AuthControllerTest extends TestCase

{
    use RefreshDatabase;

    public function setUp(): void{
        parent::setUp();
        $this->artisan('passport:install');
    }

    /**
     * Prueba básica de registrod de un usuario por parte de un administrador
     *
     *@test
     */

     public function non_authenticated_users_cannot_access_the_following_endpoints_for_users_api()
     {
        $store = $this->json('POST', '/api/auth/signup');
        $store->assertStatus(401);
     }

    /**
     * Prueba básica de registrod de un usuario por parte de un administrador
     *
     *@test
     */

    public function test_user_admin_can_sign_up_person()
    {
        // $user = User::create([
        //     'name' => 'admin',
        //     'email' => 'admin@example.com',
        //     'password' => 'pass',
        // ]);
        $user = User::factory()->create();
        $role = Role::create(['name' => 'admin']);
        $permission = Permission::create(['name' => 'admin']);
        $role->givePermissionTo($permission);
        $user->assignRole($role);

        $response = $this->ActingAs($user, 'api')->json('POST', '/api/auth/signup/', [
                'name' => 'Richard Saavedra',
                'email' => 'dev@dev.com',
                'password' => 'pass'
        ]);
        $response->assertJsonStructure(['id','name','email'])
            ->assertExactJson(['email'=>'dev@dev.com','id'=>2,'name'=>'Richard Saavedra'])
            ->assertStatus(201);
        $this->assertDatabaseHas('users', ['email' => 'dev@dev.com' ]);
    }

    /**
     * Prueba básica de registrod de un usuario por parte de un administrador
     *
     *@test
     */

    public function test_user_can_login()
    {
        $user = User::create([
            'name' => 'admin',
            'email' => 'admin@example.com',
            'password' => bcrypt('secret'),
        ]);

        $response = $this->json('POST', '/api/auth/login',[
            'email' =>  $user->email,
            'password' => 'secret',
        ]);
        $response->assertStatus(201)
            ->assertJsonStructure(['access_token','token_type','expires_at']);
    }



    // public function setUp(): void
    // {
    //     // first include all the normal setUp operations
    //     parent::setUp();

    //     // now re-register all the roles and permissions
    //     $this->app->make(\Spatie\Permission\PermissionRegistrar::class)->registerPermissions();
    // }
}
