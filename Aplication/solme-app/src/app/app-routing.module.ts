import { NgModule } from '@angular/core';
import { PreloadAllModules, RouterModule, Routes } from '@angular/router';

const routes: Routes = [
  {
    path: 'home',
    loadChildren: () => import('./home/home.module').then( m => m.HomePageModule)
  },
  {
    path: '',
    redirectTo: 'home',
    pathMatch: 'full'
  },
  {
    path: 'login',
    loadChildren: () => import('./auth/login/login.module').then( m => m.LoginPageModule)
  },
  {
    path: 'sign-up',
    loadChildren: () => import('./auth/sign-up/sign-up.module').then( m => m.SignUpPageModule)
  },
  {
    path: 'index-user',
    loadChildren: () => import('./pages/rol-user/index-user/index-user.module').then( m => m.IndexUserPageModule)
  },
  {
    path: 'tabs-user',
    loadChildren: () => import('./pages/rol-user/tabs-user/tabs-user.module').then( m => m.TabsUserPageModule)
  },
  {
    path: 'promotions-user',
    loadChildren: () => import('./pages/rol-user/promotions-user/promotions-user.module').then( m => m.PromotionsUserPageModule)
  },
  {
    path: 'profile-user',
    loadChildren: () => import('./pages/rol-user/profile-user/profile-user.module').then( m => m.ProfileUserPageModule)
  },
  {
    path: 'create-wafer-user',
    loadChildren: () => import('./pages/rol-user/create-wafer-user/create-wafer-user.module').then( m => m.CreateWaferUserPageModule)
  },
  {
    path: 'shopping-cart-user',
    loadChildren: () => import('./pages/rol-user/shopping-cart-user/shopping-cart-user.module').then( m => m.ShoppingCartUserPageModule)
  },
  {
    path: 'all-products-desserts-user',
    loadChildren: () => import('./pages/rol-user/all-products-desserts-user/all-products-desserts-user.module').then( m => m.AllProductsDessertsUserPageModule)
  },
  {
    path: 'all-products-ice-cream-glasses-user',
    loadChildren: () => import('./pages/rol-user/all-products-ice-cream-glasses-user/all-products-ice-cream-glasses-user.module').then( m => m.AllProductsIceCreamGlassesUserPageModule)
  },
  {
    path: 'info-product-user',
    loadChildren: () => import('./pages/rol-user/info-product-user/info-product-user.module').then( m => m.InfoProductUserPageModule)
  },
  {
    path: 'tabs-admin',
    loadChildren: () => import('./pages/rol-admin/tabs-admin/tabs-admin.module').then( m => m.TabsAdminPageModule)
  },
  {
    path: 'requested-orders-admin',
    loadChildren: () => import('./pages/rol-admin/requested-orders-admin/requested-orders-admin.module').then( m => m.RequestedOrdersAdminPageModule)
  },
  {
    path: 'products-admin',
    loadChildren: () => import('./pages/rol-admin/products-admin/products-admin.module').then( m => m.ProductsAdminPageModule)
  },
  {
    path: 'promotions-admin',
    loadChildren: () => import('./pages/rol-admin/promotions-admin/promotions-admin.module').then( m => m.PromotionsAdminPageModule)
  },
  {
    path: 'toppings-admin',
    loadChildren: () => import('./pages/rol-admin/toppings-admin/toppings-admin.module').then( m => m.ToppingsAdminPageModule)
  },
  {
    path: 'profile-admin',
    loadChildren: () => import('./pages/rol-admin/profile-admin/profile-admin.module').then( m => m.ProfileAdminPageModule)
  },
  {
    path: 'create-product-admin',
    loadChildren: () => import('./pages/rol-admin/create-product-admin/create-product-admin.module').then( m => m.CreateProductAdminPageModule)
  },
  {
    path: 'info-product-admin',
    loadChildren: () => import('./pages/rol-admin/info-product-admin/info-product-admin.module').then( m => m.InfoProductAdminPageModule)
  },
  {
    path: 'create-promotion-admin',
    loadChildren: () => import('./pages/rol-admin/create-promotion-admin/create-promotion-admin.module').then( m => m.CreatePromotionAdminPageModule)
  },
  

];

@NgModule({
  imports: [
    RouterModule.forRoot(routes, { preloadingStrategy: PreloadAllModules })
  ],
  exports: [RouterModule]
})
export class AppRoutingModule { }
