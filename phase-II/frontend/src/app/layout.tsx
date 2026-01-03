'use client';

import { Inter } from "next/font/google";
import { usePathname } from "next/navigation";
import "./globals.css";
import SmoothScroll from "@/components/providers/smooth-scroll";
import AuthProvider from "@/components/providers/session-provider";
import Navbar from "@/components/layout/navbar";
import Footer from "@/components/layout/footer";

const inter = Inter({ subsets: ["latin"] });

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const pathname = usePathname();
  const AuthRoutes = ['/login', '/register', '/forgot-password', '/reset-password']
  return (
    <html lang="en">
      <body className={`${inter.className} bg-slate-950 text-slate-50 antialiased selection:bg-indigo-500/30`}>
        <AuthProvider>
          <SmoothScroll>
            <Navbar/>
            <main className="flex min-h-screen flex-col overflow-hidden">
              {children}
            </main>
            {!AuthRoutes.includes(pathname) && <Footer/>}
          </SmoothScroll>
        </AuthProvider>
      </body>
    </html>
  );
}
