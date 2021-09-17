import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { IonicModule } from '@ionic/angular';

import { InfoProductAdminPage } from './info-product-admin.page';

describe('InfoProductAdminPage', () => {
  let component: InfoProductAdminPage;
  let fixture: ComponentFixture<InfoProductAdminPage>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ InfoProductAdminPage ],
      imports: [IonicModule.forRoot()]
    }).compileComponents();

    fixture = TestBed.createComponent(InfoProductAdminPage);
    component = fixture.componentInstance;
    fixture.detectChanges();
  }));

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
