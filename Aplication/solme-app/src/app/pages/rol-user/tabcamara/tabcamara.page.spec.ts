import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { IonicModule } from '@ionic/angular';

import { TabcamaraPage } from './tabcamara.page';

describe('TabcamaraPage', () => {
  let component: TabcamaraPage;
  let fixture: ComponentFixture<TabcamaraPage>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ TabcamaraPage ],
      imports: [IonicModule.forRoot()]
    }).compileComponents();

    fixture = TestBed.createComponent(TabcamaraPage);
    component = fixture.componentInstance;
    fixture.detectChanges();
  }));

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
