import { v4 as uuidv4 } from "uuid";

const CARD_DISTRIBUTION = { 1: 3, 2: 2, 3: 2, 4: 2, 5: 1 };
const COLORS = ["Red", "Blue", "Yellow", "Green", "White"];

export function createDeck() {
  const deck = [];
  for (const color of COLORS) {
    for (const [number, count] of Object.entries(CARD_DISTRIBUTION)) {
      for (let i = 0; i < count; i++) {
        deck.push({ card_id: uuidv4(), value: Number(number), color });
      }
    }
  }
  for (let i = deck.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [deck[i], deck[j]] = [deck[j], deck[i]];
  }
  return deck;
}
