import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

import { IonicModule } from '@ionic/angular';

import { CreateWaferUserPageRoutingModule } from './create-wafer-user-routing.module';

import { CreateWaferUserPage } from './create-wafer-user.page';

@NgModule({
  imports: [
    CommonModule,
    FormsModule,
    IonicModule,
    CreateWaferUserPageRoutingModule
  ],
  declarations: [CreateWaferUserPage]
})
export class CreateWaferUserPageModule {}
