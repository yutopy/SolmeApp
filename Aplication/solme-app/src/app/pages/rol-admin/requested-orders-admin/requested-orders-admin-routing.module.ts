import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { RequestedOrdersAdminPage } from './requested-orders-admin.page';

const routes: Routes = [
  {
    path: '',
    component: RequestedOrdersAdminPage
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule],
})
export class RequestedOrdersAdminPageRoutingModule {}
