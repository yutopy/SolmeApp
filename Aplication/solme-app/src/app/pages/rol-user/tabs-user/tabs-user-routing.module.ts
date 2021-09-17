import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { TabsUserPage } from './tabs-user.page';

const routes: Routes = [
  {
    path: '',
    component: TabsUserPage,
    children: [
      {
        path: 'index-user',
        loadChildren: () => import('../index-user/index-user.module').then(m => m.IndexUserPageModule)
      },
      
      {
        path: 'promotions-user',
        loadChildren: () => import('../promotions-user/promotions-user.module').then(m => m.PromotionsUserPageModule)
      },

      {
        path: 'profile-user',
        loadChildren: () => import('../profile-user/profile-user.module').then(m => m.ProfileUserPageModule)
      },
      {
        path: '',
        redirectTo: '/tabs-user/index-user',
        pathMatch: 'full'
      },
    ]
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule],
})
export class TabsUserPageRoutingModule {}
