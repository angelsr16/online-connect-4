import { Component, ElementRef, OnInit, ViewChild } from '@angular/core';
import Konva from 'konva';
import { GameBoardComponent } from '../../../../shared/konva/game-board/game-board.component';
import { Grid } from '../../../../core/models/Grid';
import { GamesService } from '../../../../core/services/games.service';
import { Game } from '../../../../core/models/db/Game';
import { ButtonModule } from 'primeng/button';
import { DialogModule } from 'primeng/dialog';
import { GamePreviewComponent } from '../../components/game-preview/game-preview.component';
import { StatusComponent } from '../../components/status/status.component';
import { CommonModule, DatePipe } from '@angular/common';
import { AuthService } from '../../../../core/services/auth.service';
import { BasicUserInfo } from '../../../../core/models/BasicUserInfo';
import { Router } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { InputTextModule } from 'primeng/inputtext';
import { MessageService } from 'primeng/api';
import { ToastModule } from 'primeng/toast';

@Component({
  selector: 'app-online',
  imports: [
    ButtonModule,
    GamePreviewComponent,
    StatusComponent,
    DatePipe,
    CommonModule,
    DialogModule,
    FormsModule,
    InputTextModule,
    ToastModule,
  ],
  providers: [MessageService],
  templateUrl: './online.component.html',
  styleUrl: './online.component.scss',
})
export class OnlineComponent {
  @ViewChild('gameBoard') gameBoard!: GameBoardComponent;

  gamesList: Game[] = [];
  gamesListToShow: Game[] = [];

  userInfo: BasicUserInfo | null;

  isLoading: boolean = false;

  currentFilter: number = 1;

  displayJoinGameModal: boolean = false;
  joinCode: string = '';

  constructor(
    private gamesService: GamesService,
    private authService: AuthService,
    private router: Router,
    private messageService: MessageService
  ) {
    this.gamesService.getGames().subscribe((games) => {
      this.gamesList = games as Game[];
      this.gamesListToShow = games as Game[];

      this.handleFilterGames(1);
    });
    this.userInfo = this.authService.getUserInfoFromToken();
  }

  onConnectGame(game: Game) {
    this.router.navigate([`/playground/online/${game.id}`]);
  }

  onNewGame() {
    this.isLoading = true;
    this.gamesService.createGame().subscribe((game: any) => {
      if (game) {
        this.router.navigate([`/playground/online/${game.id}`]);
        this.isLoading = false;
      }
    });
  }

  onJoinGame() {
    this.isLoading = true;

    this.gamesService.joinGame(this.joinCode).subscribe({
      next: (game: any) => {
        this.router.navigate([`/playground/online/${game.id}`]);
        this.isLoading = false;
      },
      error: (err) => {
        console.log(err.error);
        this.messageService.add({
          severity: 'error',
          summary: 'Error',
          detail: err.error.detail,
        });
      },
    });
  }

  handleFilterGames(filter: number) {
    this.currentFilter = filter;
    this.gamesListToShow = this.gamesList.filter((game: Game) => {
      if (filter === 0) return true;

      switch (filter) {
        case 1:
          return game.status === 'active';
        case 2:
          return game.status === 'waiting';
        case 3:
          return game.status === 'game_over';
      }

      return false;
    });
  }
}
