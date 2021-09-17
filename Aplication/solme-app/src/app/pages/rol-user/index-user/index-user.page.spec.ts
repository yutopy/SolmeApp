import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { IonicModule } from '@ionic/angular';

import { IndexUserPage } from './index-user.page';

describe('IndexUserPage', () => {
  let component: IndexUserPage;
  let fixture: ComponentFixture<IndexUserPage>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ IndexUserPage ],
      imports: [IonicModule.forRoot()]
    }).compileComponents();

    fixture = TestBed.createComponent(IndexUserPage);
    component = fixture.componentInstance;
    fixture.detectChanges();
  }));

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
