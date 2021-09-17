import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

import { IonicModule } from '@ionic/angular';

import { PromotionsUserPageRoutingModule } from './promotions-user-routing.module';

import { PromotionsUserPage } from './promotions-user.page';

@NgModule({
  imports: [
    CommonModule,
    FormsModule,
    IonicModule,
    PromotionsUserPageRoutingModule
  ],
  declarations: [PromotionsUserPage]
})
export class PromotionsUserPageModule {}
