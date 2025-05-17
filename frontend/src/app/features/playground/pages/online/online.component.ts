import { Component, ElementRef, OnInit, ViewChild } from '@angular/core';
import Konva from 'konva';
import { GameBoardComponent } from '../../../../shared/konva/game-board/game-board.component';
import { Grid } from '../../../../core/models/Grid';
import { GamesService } from '../../../../core/services/games.service';
import { Game } from '../../../../core/models/db/Game';
import { ButtonModule } from 'primeng/button';
import { GamePreviewComponent } from '../../components/game-preview/game-preview.component';
import { StatusComponent } from '../../components/status/status.component';
import { CommonModule, DatePipe } from '@angular/common';
import { AuthService } from '../../../../core/services/auth.service';
import { BasicUserInfo } from '../../../../core/models/BasicUserInfo';

@Component({
  selector: 'app-online',
  imports: [
    GameBoardComponent,
    ButtonModule,
    GamePreviewComponent,
    StatusComponent,
    DatePipe,
    CommonModule,
  ],
  templateUrl: './online.component.html',
  styleUrl: './online.component.scss',
})
export class OnlineComponent {
  @ViewChild('gameBoard') gameBoard!: GameBoardComponent;

  gamesList: Game[] = [];
  userInfo: BasicUserInfo | null;

  currentGame: Game | undefined;

  constructor(
    private gamesService: GamesService,
    private authService: AuthService
  ) {
    this.gamesService.getGames().subscribe((games) => {
      this.gamesList = games as Game[];

      console.log(this.gamesList);
    });
    this.userInfo = this.authService.getUserInfoFromToken();
  }

  placeDisc(xPos: number) {
    // var diskWasPlaced: boolean = false;
    // for (let row = this.gameGrid.length - 1; row >= 0; row--) {
    //   const cell = this.gameGrid[row][xPos];
    //   if (cell === 0) {
    //     this.gameGrid[row][xPos] = this.currentTurn;
    //     diskWasPlaced = true;
    //     this.currentTurn = this.currentTurn === 1 ? 2 : 1;
    //     break;
    //   }
    // }
    // if (diskWasPlaced) {
    //   console.log('Disk placed');
    //   this.gameBoard.updateGrid(this.gameGrid);
    // }
  }
}
