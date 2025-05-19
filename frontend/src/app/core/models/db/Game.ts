export interface Game {
  id: string;
  join_code: string;
  game_state: number[][];
  player_1: Player;
  player_2?: Player;
  current_turn: string;
  status: string;
  moves: Move[];
  created_at: Date;
  winner: string;
}

export interface Player {
  id: string;
  username: string;
  elo_rating: number;
}

export interface Move {
  player: string;
  column: number;
  row: number;
}
