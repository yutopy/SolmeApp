import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { ProfileAdminPage } from './profile-admin.page';

const routes: Routes = [
  {
    path: '',
    component: ProfileAdminPage
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule],
})
export class ProfileAdminPageRoutingModule {}
