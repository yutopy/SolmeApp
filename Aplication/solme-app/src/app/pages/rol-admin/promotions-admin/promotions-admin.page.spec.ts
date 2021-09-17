import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { IonicModule } from '@ionic/angular';

import { PromotionsAdminPage } from './promotions-admin.page';

describe('PromotionsAdminPage', () => {
  let component: PromotionsAdminPage;
  let fixture: ComponentFixture<PromotionsAdminPage>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ PromotionsAdminPage ],
      imports: [IonicModule.forRoot()]
    }).compileComponents();

    fixture = TestBed.createComponent(PromotionsAdminPage);
    component = fixture.componentInstance;
    fixture.detectChanges();
  }));

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
