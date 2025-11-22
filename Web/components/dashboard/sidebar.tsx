"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { Brain, BookOpen, BarChart3, AlertCircle, Home } from "lucide-react";
import { cn } from "@/lib/utils";

const menuItems = [
  {
    title: "Tahminler",
    href: "/dashboard",
    icon: Brain,
  },
  {
    title: "Soru Çöz",
    href: "/dashboard/soru-coz",
    icon: BookOpen,
  },
  {
    title: "İstatistiklerim",
    href: "/dashboard/istatistikler",
    icon: BarChart3,
  },
  {
    title: "Hata Analizi",
    href: "/dashboard/hata-analizi",
    icon: AlertCircle,
  },
];

export function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="hidden md:block w-64 bg-white border-r border-gray-200 min-h-screen fixed left-0 top-0 pt-20">
      <nav className="p-4 space-y-2">
        {menuItems.map((item) => {
          const Icon = item.icon;
          const isActive = pathname === item.href;
          
          return (
            <Link
              key={item.href}
              href={item.href}
              className={cn(
                "flex items-center gap-3 px-4 py-3 rounded-lg transition-colors",
                isActive
                  ? "bg-primary-50 text-primary-700 font-medium"
                  : "text-gray-700 hover:bg-gray-50"
              )}
            >
              <Icon className="w-5 h-5" />
              <span>{item.title}</span>
            </Link>
          );
        })}
      </nav>
      
      <div className="absolute bottom-4 left-4 right-4">
        <Link
          href="/"
          className="flex items-center gap-3 px-4 py-3 rounded-lg text-gray-700 hover:bg-gray-50 transition-colors"
        >
          <Home className="w-5 h-5" />
          <span>Ana Sayfa</span>
        </Link>
      </div>
    </aside>
  );
}

