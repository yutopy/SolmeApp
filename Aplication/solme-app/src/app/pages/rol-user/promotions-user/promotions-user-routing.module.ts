import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { PromotionsUserPage } from './promotions-user.page';

const routes: Routes = [
  {
    path: '',
    component: PromotionsUserPage
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule],
})
export class PromotionsUserPageRoutingModule {}
