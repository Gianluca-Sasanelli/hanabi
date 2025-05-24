import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Hanabi",
  description: "Application for the hanabi game",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={`antialiased`}>{children}</body>
    </html>
  );
}
