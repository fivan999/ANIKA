import { ComponentFixture, TestBed } from '@angular/core/testing';

import { MenuSelectTopicsComponent } from './menu-select-topics.component';

describe('MenuSelectTopicsComponent', () => {
  let component: MenuSelectTopicsComponent;
  let fixture: ComponentFixture<MenuSelectTopicsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [MenuSelectTopicsComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(MenuSelectTopicsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
