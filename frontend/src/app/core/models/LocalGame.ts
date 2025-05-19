import { Move, Player } from './db/Game';

export interface LocalGame {
  game_state: number[][];
  player_1: LocalPlayer;
  player_2: LocalPlayer;
  current_turn: number;
  moves: Move[];
  winner: number;
  isGameOver: boolean;
}

export interface LocalPlayer {
  id: number;
  username: string;
}
