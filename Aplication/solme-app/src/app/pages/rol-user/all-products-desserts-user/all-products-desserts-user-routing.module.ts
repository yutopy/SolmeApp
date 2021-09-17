import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { AllProductsDessertsUserPage } from './all-products-desserts-user.page';

const routes: Routes = [
  {
    path: '',
    component: AllProductsDessertsUserPage
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule],
})
export class AllProductsDessertsUserPageRoutingModule {}
