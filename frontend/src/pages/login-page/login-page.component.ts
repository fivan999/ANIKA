import { Component } from '@angular/core';
import { InputComponent } from "../../shared/ui/input/input.component";
import { ButtonComponent } from "../../shared/ui/button/button.component";

@Component({
  selector: 'app-login-page',
  standalone: true,
  imports: [InputComponent, ButtonComponent],
  templateUrl: './login-page.component.html',
  styleUrl: './login-page.component.less'
})
export class LoginPageComponent {

}
