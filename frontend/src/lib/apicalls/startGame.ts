import { useCardStore } from "@/store/CardStore";
import { apiRequest } from "./base";
import { Card } from "@/types/hanabi";

interface StartGameResponse {
  game_id: string;
  deck: Card[];
}

export async function startGame(): Promise<number> {
  console.log("Starting the game");
  const response = await apiRequest<StartGameResponse>("/api/start_game", {
    method: "POST",
  });

  if (response.success && response.data && response.data.deck) {
    useCardStore.getState().setCardData(response.data.deck);
  } else {
    console.error("Failed to start game:", response.error || "Unknown error");
    return 500;
  }
  return response.status;
}
