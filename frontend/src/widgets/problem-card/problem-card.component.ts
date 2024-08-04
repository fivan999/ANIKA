import { Component, Input, input } from '@angular/core';
import { CardInterface } from './problem-card.interface';


@Component({
  selector: 'app-topic-card',
  standalone: true,
  imports: [],
  templateUrl: './problem-card.component.html',
  styleUrl: './problem-card.component.less'
})
export class TopicCardComponent {
  @Input() title: string = "Спонсор"
  @Input() topic: string = "Топик"
  @Input() description: string = "Описание топика"
}
