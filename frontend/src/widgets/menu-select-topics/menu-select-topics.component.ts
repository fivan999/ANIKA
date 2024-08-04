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

}
