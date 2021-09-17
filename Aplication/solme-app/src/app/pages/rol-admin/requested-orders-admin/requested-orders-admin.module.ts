import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

import { IonicModule } from '@ionic/angular';

import { RequestedOrdersAdminPageRoutingModule } from './requested-orders-admin-routing.module';

import { RequestedOrdersAdminPage } from './requested-orders-admin.page';

@NgModule({
  imports: [
    CommonModule,
    FormsModule,
    IonicModule,
    RequestedOrdersAdminPageRoutingModule
  ],
  declarations: [RequestedOrdersAdminPage]
})
export class RequestedOrdersAdminPageModule {}
