<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

class CreateProductsTable extends Migration
{
    /**
     * Run the migrations.
     *
     * @return void
     */
    public function up()
    {
        Schema::create('products', function (Blueprint $table) {
            $table->id();
            $table->string('device_type')->default("Tablero"); 
            $table->string('device_name')->default("Futbolflex");
            $table->string('device_description')->default("Tablero para entrenamiento ubicado en...");
            $table->string('device_code');
            $table->bigInteger('user_id')->default(1);
            $table->string('status')->default("Apagado"); //Puede ser 0 Apagado, 1 Enecendido, 2 Pausa
            $table->timestamps();
        });
    }

    /**
     * Reverse the migrations.
     *
     * @return void
     */
    public function down()
    {
        Schema::dropIfExists('products');
    }
}
