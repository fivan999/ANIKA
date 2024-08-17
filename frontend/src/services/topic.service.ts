import { Injectable } from '@angular/core';
import { Router } from '@angular/router';

@Injectable({
  providedIn: 'root'
})
export class TopicService {

  constructor(private router : Router){}

  private showDetails : boolean = false;
  private correctTopic : object = {};


  getVisibilityTopicDescription() : boolean{
    return this.showDetails;
  }

  setVisibilityTopicDescription(boolean : boolean) : void{
    this.showDetails = boolean;
  }

  changeVisibilityTopicDescription() : void{
    if("/topics" == this.router.url){
      this.showDetails = true;
    }else{
      this.showDetails = !this.showDetails;

    }
  }


  setTopic(correctTopic : object){
    this.correctTopic = correctTopic;
  }

  getTopic() : object{
    return this.correctTopic;
  }
  
}
