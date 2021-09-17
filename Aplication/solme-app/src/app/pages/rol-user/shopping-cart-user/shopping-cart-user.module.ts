import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

import { IonicModule } from '@ionic/angular';

import { ShoppingCartUserPageRoutingModule } from './shopping-cart-user-routing.module';

import { ShoppingCartUserPage } from './shopping-cart-user.page';

@NgModule({
  imports: [
    CommonModule,
    FormsModule,
    IonicModule,
    ShoppingCartUserPageRoutingModule
  ],
  declarations: [ShoppingCartUserPage]
})
export class ShoppingCartUserPageModule {}
