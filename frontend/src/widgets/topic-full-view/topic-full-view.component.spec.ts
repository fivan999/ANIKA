import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TopicFullViewComponent } from './topic-full-view.component';

describe('TopicFullViewComponent', () => {
  let component: TopicFullViewComponent;
  let fixture: ComponentFixture<TopicFullViewComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [TopicFullViewComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(TopicFullViewComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
