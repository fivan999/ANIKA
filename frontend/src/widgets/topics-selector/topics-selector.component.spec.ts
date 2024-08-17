import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TopicsSelectorComponent } from './topics-selector.component';

describe('TopicsSelectorComponent', () => {
  let component: TopicsSelectorComponent;
  let fixture: ComponentFixture<TopicsSelectorComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [TopicsSelectorComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(TopicsSelectorComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
