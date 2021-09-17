import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

import { IonicModule } from '@ionic/angular';

import { ToppingsAdminPageRoutingModule } from './toppings-admin-routing.module';

import { ToppingsAdminPage } from './toppings-admin.page';

@NgModule({
  imports: [
    CommonModule,
    FormsModule,
    IonicModule,
    ToppingsAdminPageRoutingModule
  ],
  declarations: [ToppingsAdminPage]
})
export class ToppingsAdminPageModule {}
