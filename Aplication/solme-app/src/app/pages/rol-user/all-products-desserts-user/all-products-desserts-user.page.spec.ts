import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { IonicModule } from '@ionic/angular';

import { AllProductsDessertsUserPage } from './all-products-desserts-user.page';

describe('AllProductsDessertsUserPage', () => {
  let component: AllProductsDessertsUserPage;
  let fixture: ComponentFixture<AllProductsDessertsUserPage>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ AllProductsDessertsUserPage ],
      imports: [IonicModule.forRoot()]
    }).compileComponents();

    fixture = TestBed.createComponent(AllProductsDessertsUserPage);
    component = fixture.componentInstance;
    fixture.detectChanges();
  }));

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
