import { CardColor, CardValue, GameStatus } from "./enums";

export interface Card {
  id: number;
  color: CardColor;
  value: CardValue;
}

export interface Player {
  id: number;
  name: string;
  created_at?: string;
}

export interface Game {
  id: number;
  status: GameStatus;
  num_hints: number;
  num_lives: number;
  current_player_id?: number;
  created_at?: string;
  updated_at?: string;
}

export interface GamePlayer {
  game_id: number;
  player_id: number;
  player_order: number;
}

export interface GameDeck {
  id: number;
  game_id: number;
  card_id: number;
  position: number;
}

export interface PlayerHand {
  id: number;
  game_id: number;
  player_id: number;
  card_id: number;
  position: number;
  color_known: boolean;
  value_known: boolean;
}

export interface DiscardPile {
  id: number;
  game_id: number;
  card_id: number;
}

export interface PlayedCard {
  id: number;
  game_id: number;
  card_id: number;
}
