import { Component} from '@angular/core';
import { HeaderComponent } from "../../widgets/header/header.component";
import { MenuSelectTopicsComponent } from "../../widgets/menu-select-topics/menu-select-topics.component";
import { TopicsSelectorComponent } from "../../widgets/topics-selector/topics-selector.component";
import { AppComponent } from "../../app/app.component";
import { RouterOutlet, RouterLink, Router } from '@angular/router';
import { TopicService } from '../../services/topic.service';


@Component({
  selector: 'app-topics-page',
  standalone: true,
  imports: [HeaderComponent, MenuSelectTopicsComponent, TopicsSelectorComponent, AppComponent, RouterOutlet, RouterLink],
  templateUrl: './topics-page.component.html',
  styleUrl: './topics-page.component.less'
})
export class TopicsPageComponent {
[x: string]: any;


  constructor(
    private topicService: TopicService,
    private router: Router
  ){}
  
  getUrl() : string {
    return this.router.url;
  }
  getShowDetails() : boolean{
    return this.topicService.getVisibilityTopicDescription();
  }
  setShowDetails(boolean : boolean) : void{
    this.topicService.setVisibilityTopicDescription(boolean);

  }
}
