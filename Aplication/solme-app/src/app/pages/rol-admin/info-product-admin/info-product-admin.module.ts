import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

import { IonicModule } from '@ionic/angular';

import { InfoProductAdminPageRoutingModule } from './info-product-admin-routing.module';

import { InfoProductAdminPage } from './info-product-admin.page';

@NgModule({
  imports: [
    CommonModule,
    FormsModule,
    IonicModule,
    InfoProductAdminPageRoutingModule
  ],
  declarations: [InfoProductAdminPage]
})
export class InfoProductAdminPageModule {}
