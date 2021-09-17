import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { ShoppingCartUserPage } from './shopping-cart-user.page';

const routes: Routes = [
  {
    path: '',
    component: ShoppingCartUserPage
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule],
})
export class ShoppingCartUserPageRoutingModule {}
