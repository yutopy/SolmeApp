import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

import { IonicModule } from '@ionic/angular';

import { TabsUserPageRoutingModule } from './tabs-user-routing.module';

import { TabsUserPage } from './tabs-user.page';

@NgModule({
  imports: [
    CommonModule,
    FormsModule,
    IonicModule,
    TabsUserPageRoutingModule
  ],
  declarations: [TabsUserPage]
})
export class TabsUserPageModule {}
