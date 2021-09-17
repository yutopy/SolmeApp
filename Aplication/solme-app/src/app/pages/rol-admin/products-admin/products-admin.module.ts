import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

import { IonicModule } from '@ionic/angular';

import { ProductsAdminPageRoutingModule } from './products-admin-routing.module';

import { ProductsAdminPage } from './products-admin.page';

@NgModule({
  imports: [
    CommonModule,
    FormsModule,
    IonicModule,
    ProductsAdminPageRoutingModule
  ],
  declarations: [ProductsAdminPage]
})
export class ProductsAdminPageModule {}
