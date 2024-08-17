import { Component, Input, ViewEncapsulation } from '@angular/core';

@Component({
  selector: 'app-input-minimal',
  standalone: true,
  imports: [],
  template: `
  <input [placeholder]="placeholder" />
  `,
  styleUrl: './input-minimal.component.less',
})
export class InputMinimalComponent {
  @Input({
    required: true
  }) placeholder = {}
}
