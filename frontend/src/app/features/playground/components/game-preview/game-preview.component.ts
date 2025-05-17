import { CommonModule } from '@angular/common';
import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-game-preview',
  imports: [CommonModule],
  templateUrl: './game-preview.component.html',
  styleUrl: './game-preview.component.scss',
})
export class GamePreviewComponent {
  @Input() gameGrid!: number[][];
}
