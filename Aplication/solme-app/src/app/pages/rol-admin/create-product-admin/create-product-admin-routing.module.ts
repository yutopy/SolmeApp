import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { CreateProductAdminPage } from './create-product-admin.page';

const routes: Routes = [
  {
    path: '',
    component: CreateProductAdminPage
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule],
})
export class CreateProductAdminPageRoutingModule {}
