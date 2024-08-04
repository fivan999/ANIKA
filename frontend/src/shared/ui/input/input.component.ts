import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-input',
  standalone: true,
  imports: [],
  template: `
  <input [placeholder]="placeholder" />
  `,
  styleUrl: './input.component.less'
})
export class InputComponent {
  @Input({
    required: true
  }) placeholder = {}
}
