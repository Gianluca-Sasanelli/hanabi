
import { Card } from "@/types/hanabiTypes";

interface StartGameResponse {
  game_id: string;
  deck: Card[];
}

export async function startGame(): Promise<number> {
  console.log("Starting the game");
  const response = await fetch("/api/card/", {
    method: "GET",
  });
  const data = await response.json()
  if (response.ok) {
    console.log("Game started successfully")
    console.log("The response data is:", data)
  } else {
    console.error("Failed to start game:",  "Unknown error")
  }
  
  return response.status;
}