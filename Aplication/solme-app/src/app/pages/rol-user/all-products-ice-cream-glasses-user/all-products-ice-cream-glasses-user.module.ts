import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

import { IonicModule } from '@ionic/angular';

import { AllProductsIceCreamGlassesUserPageRoutingModule } from './all-products-ice-cream-glasses-user-routing.module';

import { AllProductsIceCreamGlassesUserPage } from './all-products-ice-cream-glasses-user.page';

@NgModule({
  imports: [
    CommonModule,
    FormsModule,
    IonicModule,
    AllProductsIceCreamGlassesUserPageRoutingModule
  ],
  declarations: [AllProductsIceCreamGlassesUserPage]
})
export class AllProductsIceCreamGlassesUserPageModule {}
