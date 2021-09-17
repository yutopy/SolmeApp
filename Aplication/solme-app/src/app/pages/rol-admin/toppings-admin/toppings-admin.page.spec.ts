import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { IonicModule } from '@ionic/angular';

import { ToppingsAdminPage } from './toppings-admin.page';

describe('ToppingsAdminPage', () => {
  let component: ToppingsAdminPage;
  let fixture: ComponentFixture<ToppingsAdminPage>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ToppingsAdminPage ],
      imports: [IonicModule.forRoot()]
    }).compileComponents();

    fixture = TestBed.createComponent(ToppingsAdminPage);
    component = fixture.componentInstance;
    fixture.detectChanges();
  }));

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
