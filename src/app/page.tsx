"use client";

import { useRouter } from "next/navigation";

import { Button } from "@/components/ui/button";
import { useAuth } from "./contexts/Sessions";

export default function Home() {
  const router = useRouter();
  const { sessions, isLoading } = useAuth();

  const checkSession = () => {
    if (!isLoading && sessions) {
      router.push("/game");
    } else {
      router.push("/login");
    }
  };
  return (
    <div className="relative w-full min-h-screen flex justify-center items-center bg-white overflow-hidden">
      <div className="relative z-10 text-center px-8 max-w-3xl">
        <h1 className="text-6xl md:text-7xl font-bold mb-4 text-black">
          Hanabi Game
        </h1>
        <p className="text-xl md:text-2xl text-gray-600 mb-12">
          Experience the beauty of collaboration
        </p>
        <Button
          onClick={checkSession}
          className="relative overflow-hidden px-8 py-4 text-xl bg-blue-500 rounded-full text-white font-semibold transform transition-all duration-300 hover:-translate-y-1 hover:shadow-lg focus:outline-none"
        >
          <span className="relative z-10">Enter the Game</span>
        </Button>
      </div>
    </div>
  );
}
