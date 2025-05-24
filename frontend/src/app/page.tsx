"use client";

import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import { startGame } from "@/lib/apicalls/startGame";
export default function Home() {
  const router = useRouter();

  const initGame = async () => {
    const response = await startGame();
    if (response.success) {
      router.push("/game");
    }
  };

  return (
    <div className="relative w-full min-h-screen flex justify-center items-center bg-gradient-to-br from-gray-900 to-blue-900 overflow-hidden">
      <div className="relative z-10 text-center px-8 max-w-3xl">
        <h1 className="text-6xl md:text-7xl font-bold mb-4 text-transparent bg-clip-text bg-gradient-to-r from-yellow-400 to-red-500 drop-shadow-lg">
          Hanabi Game
        </h1>
        <p className="text-xl md:text-2xl text-gray-200 mb-12">
          Experience the beauty of collaboration
        </p>
        <Button 
          onClick={initGame}
          className="relative overflow-hidden px-8 py-4 text-xl bg-gradient-to-r from-yellow-500 to-red-500 rounded-full text-white font-semibold transform transition-all duration-300 hover:-translate-y-1 hover:shadow-lg hover:shadow-red-500/40 focus:outline-none"
        >
          <span className="relative z-10">Enter the Game</span>
          <span className="absolute inset-0 bg-gradient-to-r from-yellow-400 to-red-400 opacity-0 hover:opacity-100 transition-opacity duration-300"></span>
        </Button>
      </div>
    </div>
  );
}