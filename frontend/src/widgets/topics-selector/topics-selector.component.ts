import { Component } from '@angular/core';
import { TopicCardComponent } from "../topics-card/topic-card.component";
import { TopicService } from '../../services/topic.service';
import { Router, RouterOutlet, RouterLink} from '@angular/router';
import { AuthService } from '../../services/auth.service';


@Component({
  selector: 'app-topics-selector',
  standalone: true,
  imports: [TopicCardComponent, RouterOutlet, RouterLink],
  templateUrl: './topics-selector.component.html',
  styleUrl: './topics-selector.component.less'
})
export class TopicsSelectorComponent {

  constructor(
    private authService : AuthService,
    private topicService : TopicService,
    private router : Router
  ){}

  topics: any[] = [];

  async loadTopics() {
      const response = await fetch("http://127.0.0.1:8000/topics", {
        method: "GET",
        headers: {
          "accept": "application/json",
          "Authorization": `Bearer ${this.authService.getToken()}`,
        },
      });
    
      const data = await response.json();
      this.topics = data
}
ngOnInit() {
  this.loadTopics();
}

OpenTopic(item : object){
  this.topicService.setTopic(item);
}

changeShowDetails(item : object) : void{
  this.topicService.changeVisibilityTopicDescription();
  this.OpenTopic(item);
}
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
