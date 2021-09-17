import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

import { IonicModule } from '@ionic/angular';

import { ProfileAdminPageRoutingModule } from './profile-admin-routing.module';

import { ProfileAdminPage } from './profile-admin.page';

@NgModule({
  imports: [
    CommonModule,
    FormsModule,
    IonicModule,
    ProfileAdminPageRoutingModule
  ],
  declarations: [ProfileAdminPage]
})
export class ProfileAdminPageModule {}
