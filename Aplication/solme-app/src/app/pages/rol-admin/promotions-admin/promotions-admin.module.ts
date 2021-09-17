import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

import { IonicModule } from '@ionic/angular';

import { PromotionsAdminPageRoutingModule } from './promotions-admin-routing.module';

import { PromotionsAdminPage } from './promotions-admin.page';

@NgModule({
  imports: [
    CommonModule,
    FormsModule,
    IonicModule,
    PromotionsAdminPageRoutingModule
  ],
  declarations: [PromotionsAdminPage]
})
export class PromotionsAdminPageModule {}
