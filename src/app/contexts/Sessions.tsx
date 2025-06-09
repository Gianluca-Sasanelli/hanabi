"use client";
import {
  createContext,
  useState,
  useContext,
  useEffect,
  ReactNode,
} from "react";
import { useRouter } from "next/navigation";
import { toast } from "@/hooks/use-toast";

interface Sessions {
  username: string;
}

interface AuthContextType {
  sessions: Sessions | null;
  isLoading: boolean;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
  authFetch: (url: string, options: RequestInit) => Promise<Response>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

interface AuthProviderProps {
  children: ReactNode;
}

export function AuthProvider({ children }: AuthProviderProps) {
  const [sessions, setSessions] = useState<Sessions | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const router = useRouter();

  useEffect(() => {
    console.log("Checking session");
    checkSession();
  }, []);

  const checkSession = async (): Promise<void> => {
    try {
      console.log("All cookies:", document.cookie);
      const response = await fetch("/api/login/", {
        method: "GET",
        credentials: "include",
      });

      if (response.ok) {
        const data = await response.json();
        setSessions(data);
        localStorage.setItem("sessions", JSON.stringify(data));
      } else {
        localStorage.removeItem("sessions");
        setSessions(null);
      }
    } catch (error) {
      console.error("Session check error:", error);
      localStorage.removeItem("sessions");
      setSessions(null);
    } finally {
      setIsLoading(false);
    }
  };

  const login = async (email: string, password: string): Promise<void> => {
    try {
      const response = await fetch("/api/login/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
        credentials: "include",
      });
      console.log("Response status:", response.status);
      console.log("Response headers:", [...response.headers.entries()]);
      if (!response.ok) {
        toast({
          title: "Login failed",
          description: "Please check your credentials and try again.",
          variant: "destructive",
        });

        return;
      }
      const data = await response.json();
      setSessions(data);
      localStorage.setItem("sessions", JSON.stringify(data));
      return data;
    } catch (error) {
      console.error("Login error:", error);
      throw error;
    }
  };

  const logout = (): void => {
    localStorage.removeItem("sessions");
    setSessions(null);
    router.push("/");
  };

  const authFetch = async (
    url: string,
    options: RequestInit = {},
  ): Promise<Response> => {
    const response = await fetch(url, {
      credentials: "include",
      ...options,
    });

    if (response.status === 401) {
      localStorage.removeItem("sessions");
      setSessions(null);
      router.push("/");
      toast({
        title: "Session expired",
        description: "Please login again",
        variant: "destructive",
      });
    }
    return response;
  };

  const contextValue: AuthContextType = {
    sessions,
    isLoading,
    login,
    logout,
    authFetch,
  };

  return (
    <AuthContext.Provider value={contextValue}>{children}</AuthContext.Provider>
  );
}

export const useAuth = (): AuthContextType => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
};
