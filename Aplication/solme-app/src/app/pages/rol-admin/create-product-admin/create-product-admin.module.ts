import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

import { IonicModule } from '@ionic/angular';

import { CreateProductAdminPageRoutingModule } from './create-product-admin-routing.module';

import { CreateProductAdminPage } from './create-product-admin.page';

@NgModule({
  imports: [
    CommonModule,
    FormsModule,
    IonicModule,
    CreateProductAdminPageRoutingModule
  ],
  declarations: [CreateProductAdminPage]
})
export class CreateProductAdminPageModule {}
