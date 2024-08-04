import { Component } from '@angular/core';
import { TopicCardComponent } from "../problem-card/problem-card.component";

@Component({
  selector: 'app-topics-selector',
  standalone: true,
  imports: [TopicCardComponent],
  templateUrl: './topics-selector.component.html',
  styleUrl: './topics-selector.component.less'
})
export class TopicsSelectorComponent {

}
