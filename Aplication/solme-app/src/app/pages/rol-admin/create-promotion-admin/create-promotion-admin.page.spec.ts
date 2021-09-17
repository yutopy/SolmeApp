import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { IonicModule } from '@ionic/angular';

import { CreatePromotionAdminPage } from './create-promotion-admin.page';

describe('CreatePromotionAdminPage', () => {
  let component: CreatePromotionAdminPage;
  let fixture: ComponentFixture<CreatePromotionAdminPage>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ CreatePromotionAdminPage ],
      imports: [IonicModule.forRoot()]
    }).compileComponents();

    fixture = TestBed.createComponent(CreatePromotionAdminPage);
    component = fixture.componentInstance;
    fixture.detectChanges();
  }));

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
