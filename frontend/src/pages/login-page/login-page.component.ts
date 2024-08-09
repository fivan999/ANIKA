import { Component, EventEmitter, Output } from '@angular/core';
import { InputComponent } from "../../shared/ui/input/input.component";
import { ButtonComponent } from "../../shared/ui/button/button.component";
import { FormControl, ReactiveFormsModule } from '@angular/forms';
import { Router } from '@angular/router';


@Component({
  selector: 'app-login-page',
  standalone: true,
  imports: [InputComponent, ButtonComponent, ReactiveFormsModule],
  templateUrl: './login-page.component.html',
  styleUrl: './login-page.component.less'
})
export class LoginPageComponent {


  constructor(private router: Router) { }

  ngOnInit(){
      //TODO: Добавить рефреш
      if(localStorage.getItem("access_token") !== undefined){
        this.router.navigate(['/topics']);
      }
  }
  username = new FormControl('');
  password = new FormControl('');

  async getAuthToken() : Promise<void>{
    const authTocken = await fetch("http://147.45.185.102:8000/auth/token", {
      method: 'POST',  
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        username: this.username.value,
        password: this.password.value
      })
    }).then(response => {
      if (!response.ok){
        console.log("Error: ", response.status)
      }
      return response.json();
    }).then(data => {
      console.log(data)
      localStorage.setItem("access_token", data.access_token)
      localStorage.setItem("refresh_token", data.refresh_token)

      if(data.access_token !== undefined){
        this.router.navigate(['/topics']);
      }

      return data;
    }).catch(error => {
      console.error("Error:", error);
    })
  }
}
