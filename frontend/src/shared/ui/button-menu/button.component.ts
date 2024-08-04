import { Component, Input, input } from '@angular/core';

@Component({
  selector: 'app-button-menu',
  standalone: true,
  imports: [],
  template: `
  <button tex><p>{{title}}</p><p>  ({{count}})</p></button>
  `,
  styleUrl: './button.component.less'
})
export class ButtonMenuComponent {
  @Input({
    required: true
  }) title = {};
  count = 0;
}
