import { Component, Input } from '@angular/core';


@Component({
  selector: 'app-topic-card',
  standalone: true,
  imports: [],
  templateUrl: './topic-card.component.html',
  styleUrl: './topic-card.component.less'
})
export class TopicCardComponent {
  @Input() title: string = "Спонсор"
  @Input() topic: string = "Топик"
  @Input() description: string = "Описание топика"
}
