import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

import { IonicModule } from '@ionic/angular';

import { TabcamaraPageRoutingModule } from './tabcamara-routing.module';

import { TabcamaraPage } from './tabcamara.page';

@NgModule({
  imports: [
    CommonModule,
    FormsModule,
    IonicModule,
    TabcamaraPageRoutingModule
  ],
  declarations: [TabcamaraPage]
})
export class TabcamaraPageModule {}
