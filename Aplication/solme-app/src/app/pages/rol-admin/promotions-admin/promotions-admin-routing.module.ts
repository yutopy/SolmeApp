import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { PromotionsAdminPage } from './promotions-admin.page';

const routes: Routes = [
  {
    path: '',
    component: PromotionsAdminPage
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule],
})
export class PromotionsAdminPageRoutingModule {}
