import { Component, Input, OnInit, ViewChild } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { GamesService } from '../../../../core/services/games.service';
import { Game } from '../../../../core/models/db/Game';
import { GameBoardComponent } from '../../../../shared/konva/game-board/game-board.component';
import { BasicUserInfo } from '../../../../core/models/BasicUserInfo';
import { AuthService } from '../../../../core/services/auth.service';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-game-session',
  imports: [GameBoardComponent, CommonModule],
  templateUrl: './game-session.component.html',
  styleUrl: './game-session.component.scss',
})
export class GameSessionComponent implements OnInit {
  @ViewChild('gameBoard') gameBoard!: GameBoardComponent;

  userInfo!: BasicUserInfo;
  gameId!: string | null;

  currentSocket!: WebSocket;

  gameData!: Game;

  constructor(
    private router: Router,
    private route: ActivatedRoute,
    private gamesService: GamesService,
    private authService: AuthService
  ) {
    const userInfo = this.authService.getUserInfoFromToken();

    if (userInfo !== null) {
      this.userInfo = userInfo;
    }
  }

  ngOnInit(): void {}

  ngAfterViewInit(): void {
    this.gameId = this.route.snapshot.paramMap.get('gameId');

    if (this.gameId !== null) {
      this.currentSocket = this.gamesService.connectGame(
        this.gameId,
        (gameData: any) => {
          this.gameData = gameData;
          this.gameBoard?.updateGrid(this.gameData);
        },
        (event: any) => {
          console.warn(`Closed: code=${event.code}, reason=${event.reason}`);

          if (event.code === 4004) {
            // Handle custom reason
            this.router.navigate(['/playground/online']);
            alert('Game not found or already closed.');
          }
        }
      );
    } else {
      this.router.navigate(['/playground/online']);
    }
  }

  placeDisc(xPos: number) {
    if (
      this.gameData &&
      this.gameData.status === 'active' &&
      this.gameData.current_turn === this.userInfo.uid
    ) {
      this.gamesService.makeMovement(this.gameData.id, xPos).subscribe({
        next: (game) => {
          console.log(game);
        },
        error: (err) => {
          console.log(err.error.detail);
        },
      });
    }
  }

  onCloseSession() {
    this.currentSocket?.close();
    this.router.navigate(['/playground/online']);
  }

  ngOnDestroy(): void {
    console.log('Socket closed');
    this.currentSocket?.close();
  }
}
