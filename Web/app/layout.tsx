import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "LGS Analiz ve Tahmin Asistanı",
  description: "LGS Türkçe soru analizi ve tahmin sistemi",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="tr">
      <body className={inter.className}>
        {/* Header - Tüm sayfalarda görünecek */}
        <header className="fixed top-0 left-0 right-0 bg-white border-b border-gray-200 z-50 h-20 flex items-center px-6">
          <div className="container mx-auto flex items-center justify-between">
            <h1 className="text-xl font-bold text-gray-900">
              LGS Analiz ve Tahmin Asistanı
            </h1>
            <div className="flex items-center gap-4">
              <span className="text-sm text-gray-600">Hoş geldiniz, Öğrenci</span>
            </div>
          </div>
        </header>
        {children}
      </body>
    </html>
  );
}
