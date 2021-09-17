import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { IndexUserPage } from './index-user.page';

const routes: Routes = [
  {
    path: '',
    component: IndexUserPage
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule],
})
export class IndexUserPageRoutingModule {}
