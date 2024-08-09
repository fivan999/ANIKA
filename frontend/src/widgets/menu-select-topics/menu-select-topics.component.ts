import { Component } from '@angular/core';
import { ButtonMenuComponent } from '../../shared/ui/button-menu/button.component';


@Component({
  selector: 'app-menu-select-topics',
  standalone: true,
  imports: [ButtonMenuComponent],
  templateUrl: './menu-select-topics.component.html',
  styleUrl: './menu-select-topics.component.less'
})
export class MenuSelectTopicsComponent {

  async giveAllTopics(){
    const AllTopics = await fetch("http://147.45.185.102:8000/topics",{
      method: "GET",
      headers: {"accept": "application/json",
                "'partner-id": "1",
                "Authorization": `${localStorage.getItem("access_token")}`,
      },
    }).then(response => {
      if(!response.ok){
        console.error("Error:", response.status);
      }
      return response.json();
    }).then(data => {
      console.log(data)
      return data
    }).catch(error => {
      console.error("Error:", error)
    })
  } 
}
