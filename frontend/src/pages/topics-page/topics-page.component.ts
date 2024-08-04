import { Component } from '@angular/core';
import { HeaderComponent } from "../../widgets/header/header.component";
import { MenuSelectTopicsComponent } from "../../widgets/menu-select-topics/menu-select-topics.component";
import { TopicsSelectorComponent } from "../../widgets/topics-selector/topics-selector.component";

@Component({
  selector: 'app-topics-page',
  standalone: true,
  imports: [HeaderComponent, MenuSelectTopicsComponent, TopicsSelectorComponent],
  templateUrl: './topics-page.component.html',
  styleUrl: './topics-page.component.less'
})
export class TopicsPageComponent {

}
