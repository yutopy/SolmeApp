import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

import { IonicModule } from '@ionic/angular';

import { InfoProductUserPageRoutingModule } from './info-product-user-routing.module';

import { InfoProductUserPage } from './info-product-user.page';

@NgModule({
  imports: [
    CommonModule,
    FormsModule,
    IonicModule,
    InfoProductUserPageRoutingModule
  ],
  declarations: [InfoProductUserPage]
})
export class InfoProductUserPageModule {}
