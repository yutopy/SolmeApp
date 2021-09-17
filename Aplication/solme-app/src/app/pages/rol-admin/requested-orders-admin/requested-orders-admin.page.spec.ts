import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { IonicModule } from '@ionic/angular';

import { RequestedOrdersAdminPage } from './requested-orders-admin.page';

describe('RequestedOrdersAdminPage', () => {
  let component: RequestedOrdersAdminPage;
  let fixture: ComponentFixture<RequestedOrdersAdminPage>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ RequestedOrdersAdminPage ],
      imports: [IonicModule.forRoot()]
    }).compileComponents();

    fixture = TestBed.createComponent(RequestedOrdersAdminPage);
    component = fixture.componentInstance;
    fixture.detectChanges();
  }));

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
