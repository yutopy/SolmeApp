import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

import { IonicModule } from '@ionic/angular';

import { IndexUserPageRoutingModule } from './index-user-routing.module';

import { IndexUserPage } from './index-user.page';

@NgModule({
  imports: [
    CommonModule,
    FormsModule,
    IonicModule,
    IndexUserPageRoutingModule
  ],
  declarations: [IndexUserPage]
})
export class IndexUserPageModule {}
