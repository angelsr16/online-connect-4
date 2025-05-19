import { Component, OnInit, ViewChild } from '@angular/core';
import { GameBoardComponent } from '../../../../shared/konva/game-board/game-board.component';
import { Game } from '../../../../core/models/db/Game';
import { LocalGame } from '../../../../core/models/LocalGame';
import { LocalGameBoardComponent } from '../../../../shared/konva/local-game-board/local-game-board.component';
import { CommonModule } from '@angular/common';
import { Grid } from '../../../../core/models/Grid';
import { ButtonModule } from 'primeng/button';
import confetti from 'canvas-confetti';

@Component({
  selector: 'app-local',
  imports: [LocalGameBoardComponent, CommonModule, ButtonModule],
  templateUrl: './local.component.html',
  styleUrl: './local.component.scss',
})
export class LocalComponent implements OnInit {
  @ViewChild('gameBoard') gameBoard!: LocalGameBoardComponent;
  currentGame!: LocalGame;

  gameOverMessage: string = '';

  constructor() {}

  ngOnInit(): void {
    this.initGame();
  }

  initGame() {
    this.currentGame = {
      game_state: [
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
      ],
      player_1: {
        id: 1,
        username: 'Player 1',
      },
      player_2: {
        id: 2,
        username: 'Player 2',
      },
      current_turn: 1,
      moves: [],
      winner: 0,
      isGameOver: false,
    };

    this.gameBoard?.updateGame(this.currentGame);
  }

  placeDisc(columnIndex: number) {
    if (this.currentGame.isGameOver) return;
    let diskWasPlaced = false;
    var gameStatus = null;

    for (let row = this.currentGame.game_state.length - 1; row >= 0; row--) {
      let cell = this.currentGame.game_state[row][columnIndex];
      if (cell === 0) {
        this.currentGame.game_state[row][columnIndex] =
          this.currentGame.current_turn;

        gameStatus = this.checkGameStatus(
          this.currentGame.game_state,
          this.currentGame.current_turn
        );

        if (gameStatus === 'win') {
          this.gameOverMessage = `PLAYER ${this.currentGame.current_turn} WON!`;
        } else if (gameStatus === 'draw') {
          this.gameOverMessage = 'DRAW';
        } else {
          this.currentGame.current_turn =
            this.currentGame.current_turn === this.currentGame.player_1.id
              ? this.currentGame.player_2.id
              : this.currentGame.player_1.id;
        }

        diskWasPlaced = true;
        break;
      }
    }

    if (diskWasPlaced) {
      this.gameBoard.updateGame(this.currentGame);

      this.currentGame.isGameOver = gameStatus !== null;

      if (this.currentGame.isGameOver) {
        confetti({
          particleCount: 500,
          spread: 300,
          origin: {
            y: 0.5,
          },
        });
      }
    }
  }

  checkGameStatus(gameGrid: Grid, player: number) {
    const rows = gameGrid.length;
    const cols = gameGrid[0].length;

    // Horizontal
    for (let row = 0; row < rows; row++) {
      for (let col = 0; col <= cols - 4; col++) {
        if (
          gameGrid[row].slice(col, col + 4).every((cell) => cell === player)
        ) {
          return 'win';
        }
      }
    }

    // Vertical
    for (let row = 0; row <= rows - 4; row++) {
      for (let col = 0; col < cols; col++) {
        if (
          gameGrid[row][col] === player &&
          gameGrid[row + 1][col] === player &&
          gameGrid[row + 2][col] === player &&
          gameGrid[row + 3][col] === player
        ) {
          return 'win';
        }
      }
    }

    // Diagonal (\)
    for (let row = 0; row <= rows - 4; row++) {
      for (let col = 0; col <= cols - 4; col++) {
        if (
          gameGrid[row][col] === player &&
          gameGrid[row + 1][col + 1] === player &&
          gameGrid[row + 2][col + 2] === player &&
          gameGrid[row + 3][col + 3] === player
        ) {
          return 'win';
        }
      }
    }

    // Diagonal (/)
    for (let row = 0; row <= rows - 4; row++) {
      for (let col = 3; col < cols; col++) {
        if (
          gameGrid[row][col] === player &&
          gameGrid[row + 1][col - 1] === player &&
          gameGrid[row + 2][col - 2] === player &&
          gameGrid[row + 3][col - 3] === player
        ) {
          return 'win';
        }
      }
    }

    // Draw
    const isDraw = gameGrid.every((row) => row.every((cell) => cell !== 0));
    if (isDraw) return 'draw';

    return null;
  }
}
