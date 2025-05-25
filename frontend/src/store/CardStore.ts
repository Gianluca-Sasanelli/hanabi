import { create } from "zustand";
import { persist } from "zustand/middleware";
import { Card } from "@/types/hanabi";

interface CardStore {
  // State
  cards: Card[];
  isHydrated: boolean;
  setHydrated: (isHydrated: boolean) => void;

  // Setters
  setCardData: (cards: Card[]) => void;
  addCard: (card: Card) => void;
  removeCard: (cardId: string) => void;
  updateCard: (cardId: string, updates: Partial<Card>) => void;

  // Selectors
  getCardById: (id: string) => Card | undefined;
}

export const useCardStore = create<CardStore>()(
  persist(
    (set, get) => ({
      // State
      cards: [],
      isHydrated: false,
      setHydrated: (isHydrated: boolean) => set({ isHydrated }),

      // Setters
      setCardData: (cards) => set({ cards }),

      addCard: (card) =>
        set((state) => ({
          cards: [...state.cards, card],
        })),

      removeCard: (cardId) =>
        set((state) => ({
          cards: state.cards.filter((c) => c.cardId !== cardId),
        })),

      updateCard: (cardId, updates) =>
        set((state) => ({
          cards: state.cards.map((c) =>
            c.cardId === cardId ? { ...c, ...updates } : c,
          ),
        })),

      // Selectors
      getCardById: (id) => get().cards.find((c) => c.cardId === id),
    }),
    {
      name: "card-storage",
      onRehydrateStorage: () => (state) => {
        if (state) {
          state.setHydrated(true);
        }
      },
    },
  ),
);
