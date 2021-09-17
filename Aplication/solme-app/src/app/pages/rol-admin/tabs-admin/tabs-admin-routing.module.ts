import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { TabsAdminPage } from './tabs-admin.page';

const routes: Routes = [
  {
    path: '',
    component: TabsAdminPage,
    children: [
      {
        path: 'requested-orders-admin',
        loadChildren: () => import('../requested-orders-admin/requested-orders-admin.module').then(m => m.RequestedOrdersAdminPageModule)
      },
      
      {
        path: 'products-admin',
        loadChildren: () => import('../products-admin/products-admin.module').then(m => m.ProductsAdminPageModule)

      },

      {
        path: 'promotions-admin',
        loadChildren: () => import('../promotions-admin/promotions-admin.module').then(m => m.PromotionsAdminPageModule)
      },
      {
        path: '',
        redirectTo: '/tabs-admin/requested-orders-admin',
        pathMatch: 'full'
      },
    ]
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule],
})
export class TabsAdminPageRoutingModule {}
