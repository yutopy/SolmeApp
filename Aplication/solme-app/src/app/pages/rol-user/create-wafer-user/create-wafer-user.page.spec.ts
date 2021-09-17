import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { IonicModule } from '@ionic/angular';

import { CreateWaferUserPage } from './create-wafer-user.page';

describe('CreateWaferUserPage', () => {
  let component: CreateWaferUserPage;
  let fixture: ComponentFixture<CreateWaferUserPage>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ CreateWaferUserPage ],
      imports: [IonicModule.forRoot()]
    }).compileComponents();

    fixture = TestBed.createComponent(CreateWaferUserPage);
    component = fixture.componentInstance;
    fixture.detectChanges();
  }));

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
