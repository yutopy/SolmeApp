import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { InfoProductAdminPage } from './info-product-admin.page';

const routes: Routes = [
  {
    path: '',
    component: InfoProductAdminPage
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule],
})
export class InfoProductAdminPageRoutingModule {}
