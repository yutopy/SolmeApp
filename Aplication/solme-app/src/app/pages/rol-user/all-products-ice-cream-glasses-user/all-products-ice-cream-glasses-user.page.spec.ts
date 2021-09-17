import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { IonicModule } from '@ionic/angular';

import { AllProductsIceCreamGlassesUserPage } from './all-products-ice-cream-glasses-user.page';

describe('AllProductsIceCreamGlassesUserPage', () => {
  let component: AllProductsIceCreamGlassesUserPage;
  let fixture: ComponentFixture<AllProductsIceCreamGlassesUserPage>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ AllProductsIceCreamGlassesUserPage ],
      imports: [IonicModule.forRoot()]
    }).compileComponents();

    fixture = TestBed.createComponent(AllProductsIceCreamGlassesUserPage);
    component = fixture.componentInstance;
    fixture.detectChanges();
  }));

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
