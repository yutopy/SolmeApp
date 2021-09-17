import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { AllProductsIceCreamGlassesUserPage } from './all-products-ice-cream-glasses-user.page';

const routes: Routes = [
  {
    path: '',
    component: AllProductsIceCreamGlassesUserPage
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule],
})
export class AllProductsIceCreamGlassesUserPageRoutingModule {}
