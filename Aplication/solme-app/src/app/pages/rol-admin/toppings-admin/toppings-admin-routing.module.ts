import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { ToppingsAdminPage } from './toppings-admin.page';

const routes: Routes = [
  {
    path: '',
    component: ToppingsAdminPage
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule],
})
export class ToppingsAdminPageRoutingModule {}
