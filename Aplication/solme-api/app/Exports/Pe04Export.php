<?php

namespace App\Exports;

use App\Pe04;
use Maatwebsite\Excel\Concerns\FromCollection;

class Pe04Export implements FromCollection
{
    /**
    * @return \Illuminate\Support\Collection
    */
    public function collection()
    {
        return Pe04::all();
    }
}
