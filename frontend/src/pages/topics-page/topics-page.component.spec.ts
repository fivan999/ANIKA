import { ComponentFixture, TestBed } from '@angular/core/testing';
import { RouterOutlet } from '@angular/router';


import { TopicsPageComponent } from './topics-page.component';

describe('TopicsPageComponent', () => {
  let component: TopicsPageComponent;
  let fixture: ComponentFixture<TopicsPageComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [TopicsPageComponent, RouterOutlet]
    })
    .compileComponents();

    fixture = TestBed.createComponent(TopicsPageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
