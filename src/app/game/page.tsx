import GamePage from "@/components/Game/GamePage";
import { ProtectedRoute } from "@/components/ProtectedRoute";

export default function Game() {
  return (
    <ProtectedRoute>
      <GamePage />
    </ProtectedRoute>
  );
}
