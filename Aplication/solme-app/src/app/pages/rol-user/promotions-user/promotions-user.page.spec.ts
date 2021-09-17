import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { IonicModule } from '@ionic/angular';

import { PromotionsUserPage } from './promotions-user.page';

describe('PromotionsUserPage', () => {
  let component: PromotionsUserPage;
  let fixture: ComponentFixture<PromotionsUserPage>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ PromotionsUserPage ],
      imports: [IonicModule.forRoot()]
    }).compileComponents();

    fixture = TestBed.createComponent(PromotionsUserPage);
    component = fixture.componentInstance;
    fixture.detectChanges();
  }));

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
