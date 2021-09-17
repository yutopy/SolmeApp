import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { CreateWaferUserPage } from './create-wafer-user.page';

const routes: Routes = [
  {
    path: '',
    component: CreateWaferUserPage
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule],
})
export class CreateWaferUserPageRoutingModule {}
