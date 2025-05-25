import { create } from "zustand";
import { persist } from "zustand/middleware";
import { Card } from "@/types/hanabiTypes";

interface CardStore {
  // State
  cards: Card[];
  isHydrated: boolean;
  setHydrated: (isHydrated: boolean) => void;

  // Setters
  setCardData: (cards: Card[]) => void;
  addCard: (card: Card) => void;
  removeCard: (cardId: number) => void;
  updateCard: (cardId: number, updates: Partial<Card>) => void;

  // Selectors
  getCardById: (id: number) => Card | undefined;
}

export const useCardStore = create<CardStore>()(
  persist(
    (set, get) => ({
      cards: [],
      isHydrated: false,
      setHydrated: (isHydrated: boolean) => set({ isHydrated }),

      setCardData: (cards) => set({ cards }),

      addCard: (card) =>
        set((state) => ({
          cards: [...state.cards, card],
        })),

      removeCard: (cardId) =>
        set((state) => ({
          cards: state.cards.filter((c) => c.id !== cardId),
        })),

      updateCard: (cardId, updates) =>
        set((state) => ({
          cards: state.cards.map((c) =>
            c.id === cardId ? { ...c, ...updates } : c,
          ),
        })),

      // Selectors
      getCardById: (id) => get().cards.find((c) => c.id === id),
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
