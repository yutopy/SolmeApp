import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

import { IonicModule } from '@ionic/angular';

import { AllProductsDessertsUserPageRoutingModule } from './all-products-desserts-user-routing.module';

import { AllProductsDessertsUserPage } from './all-products-desserts-user.page';

@NgModule({
  imports: [
    CommonModule,
    FormsModule,
    IonicModule,
    AllProductsDessertsUserPageRoutingModule
  ],
  declarations: [AllProductsDessertsUserPage]
})
export class AllProductsDessertsUserPageModule {}
