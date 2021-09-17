import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { IonicModule } from '@ionic/angular';

import { InfoProductUserPage } from './info-product-user.page';

describe('InfoProductUserPage', () => {
  let component: InfoProductUserPage;
  let fixture: ComponentFixture<InfoProductUserPage>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ InfoProductUserPage ],
      imports: [IonicModule.forRoot()]
    }).compileComponents();

    fixture = TestBed.createComponent(InfoProductUserPage);
    component = fixture.componentInstance;
    fixture.detectChanges();
  }));

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
