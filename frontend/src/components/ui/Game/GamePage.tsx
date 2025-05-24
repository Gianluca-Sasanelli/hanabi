// HanabiGamePage.tsx
"use client";

import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { useCardStore } from "@/store/CardStore";

// Define card colors
const cardColors = {
  red: "bg-red-500",
  blue: "bg-blue-500",
  green: "bg-green-500",
  yellow: "bg-yellow-500",
  white: "bg-gray-200"
};

const PlayerHand = ({ playerName, isCurrentPlayer = false }: { playerName: string, isCurrentPlayer: boolean }) => {
  const dummyCards = [1, 2, 3, 4, 5];
  
  return (
    <div className={`p-4 rounded-lg ${isCurrentPlayer ? "bg-slate-200" : "bg-slate-100"}`}>
      <div className="flex justify-between items-center mb-4">
        <h3 className="text-lg font-bold">{playerName}</h3>
        {isCurrentPlayer && <Badge variant="outline" className="bg-green-100">Your Turn</Badge>}
      </div>
      
      <div className="flex gap-2 justify-center">
        {dummyCards.map((_, index) => (
          <div 
            key={index} 
            className="w-16 h-24 rounded-lg bg-white border-2 border-slate-300 flex items-center justify-center shadow-md"
          >
            <span className="text-xl font-bold text-gray-400">?</span>
          </div>
        ))}
      </div>
    </div>
  );
};

const GameTable = () => {
  return (
    <div className="bg-green-800 p-6 rounded-xl shadow-xl mb-8">
      <h3 className="text-white text-lg font-bold mb-4">Fireworks</h3>
      <div className="flex gap-4 justify-center mb-6">
        {Object.entries(cardColors).map(([color, bgClass]) => (
          <div key={color} className="flex flex-col items-center">
            <div className={`w-16 h-24 ${bgClass} rounded-lg shadow-md flex items-center justify-center`}>
              <span className="text-xl font-bold text-white">-</span>
            </div>
            <span className="text-white mt-2 capitalize">{color}</span>
          </div>
        ))}
      </div>
      
      <div className="flex justify-between items-center bg-green-700 p-4 rounded-lg">
        <div>
          <h4 className="text-white text-sm mb-1">Hint Tokens</h4>
          <div className="flex gap-1">
            {[...Array(8)].map((_, i) => (
              <div key={i} className="w-6 h-6 rounded-full bg-blue-400 border border-blue-600"></div>
            ))}
          </div>
        </div>
        
        <div>
          <h4 className="text-white text-sm mb-1">Lifes</h4>
          <div className="flex gap-1">
            {[...Array(3)].map((_, i) => (
              <div key={i} className="w-6 h-6 rounded-full bg-red-500 border border-red-700"></div>
            ))}
          </div>
        </div>
        
        <div className="text-center">
          <h4 className="text-white text-sm mb-1">Deck</h4>
          <div className="bg-slate-300 w-10 h-14 rounded-md border-2 border-slate-400 flex items-center justify-center">
            <span className="text-sm font-bold">50</span>
          </div>
        </div>
      </div>
    </div>
  );
};

const GameActions = () => {
  return (
    <div className="flex gap-3 justify-center mb-8">
      <Button variant="outline">Give Hint</Button>
      <Button variant="destructive">Discard Card</Button>
      <Button variant="default">Play Card</Button>
    </div>
  );
};

export default function HanabiGamePage() {
  const { cards } = useCardStore();
  console.log(cards)
  return (
    <div className="container mx-auto py-8 max-w-4xl">
      <h1 className="text-3xl font-bold text-center mb-8">Hanabi</h1>
      
      <PlayerHand playerName="Player 2" isCurrentPlayer={false} />
      <div className="my-8">
        <GameTable />
      </div>
      <GameActions />
      <PlayerHand playerName="Player 1 (You)" isCurrentPlayer={true} />
    </div>
  );
}