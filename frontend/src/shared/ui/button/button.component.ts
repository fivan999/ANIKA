import { Component, Input, input } from '@angular/core';

@Component({
  selector: 'app-button',
  standalone: true,
  imports: [],
  template: `
  <button tex>{{title}}</button>
  `,
  styleUrl: './button.component.less'
})
export class ButtonComponent {
  @Input({
    required: true
  }) title = {};
}
