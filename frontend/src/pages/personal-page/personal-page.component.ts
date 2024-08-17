import { Component } from '@angular/core';
import { HeaderComponent } from "../../widgets/header/header.component";
import { InputMinimalComponent } from "../../shared/ui/input-minimal/input-minimal.component";
import { RouterLink } from '@angular/router';
import { AuthService } from '../../services/auth.service';
import { ReactiveFormsModule, FormControl } from '@angular/forms';



interface User {
  username: string;
  email: string;
  id: number;
  partner_id: number;
}

@Component({
  selector: 'app-personal-page',
  standalone: true,
  imports: [HeaderComponent, InputMinimalComponent, RouterLink, ReactiveFormsModule],
  templateUrl: './personal-page.component.html',
  styleUrl: './personal-page.component.less'
})  

export class PersonalPageComponent {

  constructor(private authService : AuthService){}

  user: User = {} as User;
  partner : any = {};
  topics : any = {};
  allURLsSubscriptions : any = {};
  openCreateTopic : boolean = false;
  openAddPermission : boolean = false;
  openPermisionEditor : boolean = false;
  
  topicName = new FormControl("");
  topicDescription = new FormControl("");

  ngOnInit(){
    this.getUser();
    this.getMyTopics();
    this.getMySubscriptions();
  }
  changeCreateTopic(){
    this.openCreateTopic = !this.openCreateTopic;
  }
  changeOpenPermisionEditor(){
    this.openPermisionEditor = !this.openPermisionEditor;
  }

  async getUser() {
    try {
      const response = await fetch("http://127.0.0.1:8000/auth/me", {
        method: "GET",
        headers: {
          "accept": "application/json",
          "Authorization": `Bearer ${this.authService.getToken()}`
        }
      });
      const data = await response.json();
      this.user = data;
      console.log(data)


      try {
        const response = await fetch(`http://127.0.0.1:8000/partners/${this.user.partner_id}`, {
          method: "GET",
          headers: {
            "accept": "application/json",
            "Authorization": `Bearer ${this.authService.getToken()}`
          }
        });
        const data = await response.json();
        this.partner = data;
      } catch (e) {
        console.error(e);
      }


    } catch (e) {
      console.error(e);
    }
  }
  async getMyTopics() {
    try {
      const response = await fetch(`http://127.0.0.1:8000/topics/my`, {
        method: "GET",
        headers: {
          "accept": "application/json",
          "Authorization": `Bearer ${this.authService.getToken()}`
        }
      });
      const data = await response.json();
      this.topics = data;
    } catch (e) {
      console.error(e);
    }
  }
  async removeTopic(id : number) {
    try {
      const response = await fetch(`http://127.0.0.1:8000/topics/${id}`, {
        method: "DELETE",
        headers: {
          "accept": "application/json",
          "Authorization": `Bearer ${this.authService.getToken()}`
        }
      });
      const data = await response.json();
      this.topics = this.topics.filter((item: { id: number; }) => item.id !== id);

    } catch (e) {
      console.error(e);
    }
  }
  async createTopic() {
    try {
      const response = await fetch(`http://127.0.0.1:8000/topics/create`, {
        method: "POST",
        headers: {
          "accept": "application/json",
          'Content-Type': 'application/json',
          "Authorization": `Bearer ${this.authService.getToken()}`
        },
        body: JSON.stringify({
          name: "fwefwf",
          description: "fewfw",
          json_template: {
            title: "Sample Template",
            version: 1.0,
            components: [
              {
                type: "header",
                content: "This is the header"
              },
              {
                type: "paragraph",
                content: "This is a paragraph in the template."
              },
              {
                type: "footer",
                content: "This is the footer"
              }
            ],
            metadata: {
              createdBy: "User123",
            }
          }
        })
      });
      
      const data = await response.json();
  
    } catch (e) {
      console.error(e);
    }
  }
  async getMySubscriptions() {
    try {
      const response = await fetch(`http://127.0.0.1:8000/subscriptions/my`, {
        method: "GET",
        headers: {
          "accept": "application/json",
          "Authorization": `Bearer ${this.authService.getToken()}`
        }
      });
      const data = await response.json();
      this.allURLsSubscriptions = data;
    } catch (e) {
      console.error(e);
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
    this.allURLsSubscriptions = this.allURLsSubscriptions.filter((item: { id: number; }) => item.id !== id);


  }catch(e){
    console.error(e)
  }
}
}
