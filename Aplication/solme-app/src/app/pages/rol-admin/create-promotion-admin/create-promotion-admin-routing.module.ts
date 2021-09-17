import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { CreatePromotionAdminPage } from './create-promotion-admin.page';

const routes: Routes = [
  {
    path: '',
    component: CreatePromotionAdminPage
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule],
})
export class CreatePromotionAdminPageRoutingModule {}
