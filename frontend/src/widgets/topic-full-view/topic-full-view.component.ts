import { Component } from '@angular/core';
import { RouterLink } from '@angular/router';
import { TopicService } from '../../services/topic.service';
import { InputMinimalComponent } from "../../shared/ui/input-minimal/input-minimal.component";
import { AuthService } from '../../services/auth.service';
import { FormControl, ReactiveFormsModule } from '@angular/forms';


interface Topic {
  name: string;
  description: string;
  id: number;
  partner: {
    name: string;
  }
}

@Component({
  selector: 'app-topic-full-view',
  standalone: true,
  imports: [RouterLink, InputMinimalComponent, ReactiveFormsModule],
  templateUrl: './topic-full-view.component.html',
  styleUrl: './topic-full-view.component.less'
})



export class TopicFullViewComponent {
  topic: Topic;
  URLsSubscriptions: any[] = [];
  topicMessenges: any = {};
  addInput = new FormControl('https://');

  constructor(
    private topicService: TopicService,
    private authService: AuthService
  ){
    this.topic = this.giveTopic(); 
  }

  ngOnInit(){
    this.giveUrls();
    console.log(this.URLsSubscriptions)
    this.messagesSearch()
  }

  changeTopicVisible(){
    this.topicService.changeVisibilityTopicDescription();
  }

  giveTopic(): Topic {
    return this.topicService.getTopic() as Topic;
  }


  async giveUrls(){
    try{
    const response = await fetch(`http://147.45.185.102:8000/subscriptions/topic/${this.topic.id}`, {
      method: "GET",
      headers: {
        "accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": `Bearer ${this.authService.getToken()}`,

      }
    })
    const data = await response.json();
    this.URLsSubscriptions = data
  }catch(e){
    console.error("Error: ", e)
  }
    
  }

  async CreateUrls(){
    try{
    const response = await fetch(`http://147.45.185.102:8000/subscriptions/create`, {
      method: "POST",
      headers: {
        "accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": `Bearer ${this.authService.getToken()}`,
      },
      body: JSON.stringify({
        "topic_id": this.topic.id,
        "url": `${this.addInput.value}`
      })
    })
    const data = await response.json();
    console.log(data);
    this.URLsSubscriptions.push(data);
  }catch(e){
    console.error("Error: ", e)
  }
    
  }
  async messagesSearch(){
    try{
    const response = await fetch(`http://127.0.0.1:8000/messages/search`, {
      method: "POST",
      headers: {
        "accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": `Bearer ${this.authService.getToken()}`,
      },
      body: JSON.stringify({
        "topic_ids": [
          this.topic.id
        ],
      })
    })
    const data = await response.json();
    console.log(data);
    this.topicMessenges = data;
  }catch(e){
    console.error("Error: ", e)
  }
    
  }


  async unSubscription(id : number){

    try{
    const response = await fetch(
      `http://127.0.0.1:8000/subscriptions/delete/${id}`, {
      method: "DELETE",
      headers: {"accept": "application/json",
                "Authorization": `Bearer ${this.authService.getToken()}`,
    },
      })
    const data = await response.json();
    this.URLsSubscriptions = this.URLsSubscriptions.filter(item => item.id !== id);


  }catch(e){
    console.error(e)
  }
}
}
