"use client";

import { useAuth } from "@/app/contexts/Sessions";
import { useRouter } from "next/navigation";
import { useEffect } from "react";

interface ProtectedRouteProps {
  children: React.ReactNode;
}

export function ProtectedRoute({ children }: ProtectedRouteProps) {
  const { sessions, isLoading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!isLoading && !sessions) {
      router.push("/login");
    }
  }, [sessions, isLoading, router]);

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-gray-900"></div>
      </div>
    );
  }

  if (!sessions) {
    return null;
  }

  return <>{children}</>;
}
