import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { TabcamaraPage } from './tabcamara.page';

const routes: Routes = [
  {
    path: '',
    component: TabcamaraPage
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule],
})
export class TabcamaraPageRoutingModule {}
