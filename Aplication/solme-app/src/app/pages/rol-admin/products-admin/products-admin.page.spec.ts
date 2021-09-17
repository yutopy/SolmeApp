import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { IonicModule } from '@ionic/angular';

import { ProductsAdminPage } from './products-admin.page';

describe('ProductsAdminPage', () => {
  let component: ProductsAdminPage;
  let fixture: ComponentFixture<ProductsAdminPage>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ProductsAdminPage ],
      imports: [IonicModule.forRoot()]
    }).compileComponents();

    fixture = TestBed.createComponent(ProductsAdminPage);
    component = fixture.componentInstance;
    fixture.detectChanges();
  }));

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
