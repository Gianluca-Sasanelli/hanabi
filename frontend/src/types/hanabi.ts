export type CardColor = "Red" | "Blue" | "Yellow" | "Green" | "White";
export type CardValue = 1 | 2 | 3 | 4 | 5;
export type HintType = "color" | "number";

export type Card = {
  cardId: string;
  value: CardValue;
  color: CardColor;
};

export type Board = {
  cards: Card[];
  numHints: number;
  numLifes: number;
};
