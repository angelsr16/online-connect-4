import { Component, ElementRef, OnInit, ViewChild } from '@angular/core';
import Konva from 'konva';
import { GameBoardComponent } from '../../../shared/konva/game-board/game-board.component';
import { Grid } from '../../../core/models/Grid';

@Component({
  selector: 'app-online',
  imports: [GameBoardComponent],
  templateUrl: './online.component.html',
  styleUrl: './online.component.scss',
})
export class OnlineComponent {
  @ViewChild('gameBoard') gameBoard!: GameBoardComponent;

  currentTurn: number = 1;

  gameGrid: Grid = [
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [2, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0],
  ];

  placeDisc(xPos: number) {
    var diskWasPlaced: boolean = false;
    for (let row = this.gameGrid.length - 1; row >= 0; row--) {
      const cell = this.gameGrid[row][xPos];
      if (cell === 0) {
        this.gameGrid[row][xPos] = this.currentTurn;
        diskWasPlaced = true;
        this.currentTurn = this.currentTurn === 1 ? 2 : 1;
        break;
      }
    }

    if (diskWasPlaced) {
      console.log('Disk placed');
      this.gameBoard.updateGrid(this.gameGrid);
    }
  }
}
