import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

import { IonicModule } from '@ionic/angular';

import { CreatePromotionAdminPageRoutingModule } from './create-promotion-admin-routing.module';

import { CreatePromotionAdminPage } from './create-promotion-admin.page';

@NgModule({
  imports: [
    CommonModule,
    FormsModule,
    IonicModule,
    CreatePromotionAdminPageRoutingModule
  ],
  declarations: [CreatePromotionAdminPage]
})
export class CreatePromotionAdminPageModule {}
