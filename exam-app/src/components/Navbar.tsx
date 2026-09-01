"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { BookOpen, LogOut, User, BarChart3, CreditCard } from "lucide-react";
import { useEffect, useState } from "react";

export default function Navbar() {
    const router = useRouter();
    const [username, setUsername] = useState<string | null>(null);

    useEffect(() => {
        const storedUser = localStorage.getItem("user");
        if (storedUser) {
            try {
                const parsedUser = JSON.parse(storedUser);
                setUsername(parsedUser.username || parsedUser.full_name || "Student");
            } catch (e) {
                // If it's just a string or parsing fails, use it as is or fallback
                setUsername(storedUser);
            }
        }
    }, []);

    const handleLogout = () => {
        localStorage.removeItem("user");
        router.push("/");
    };

    return (
        <nav className="border-b border-slate-800 bg-slate-900/50 backdrop-blur-md sticky top-0 z-50">
            <div className="container h-16 flex items-center justify-between">
                <Link href="/dashboard" className="flex items-center gap-2 font-bold text-xl">
                    <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-primary to-accent flex items-center justify-center">
                        <BookOpen size={18} className="text-white" />
                    </div>
                    <span className="bg-clip-text text-transparent bg-gradient-to-r from-white to-slate-400">
                        ExamAI
                    </span>
                </Link>

                <div className="flex items-center gap-6">
                    {/* Navigation Links */}
                    <Link 
                        href="/performance" 
                        className="flex items-center gap-2 px-3 py-1.5 text-sm text-slate-400 hover:text-white transition-colors"
                    >
                        <BarChart3 size={16} />
                        <span>Performance</span>
                    </Link>
                    <Link 
                        href="/subscription" 
                        className="flex items-center gap-2 px-3 py-1.5 text-sm text-slate-400 hover:text-white transition-colors"
                    >
                        <CreditCard size={16} />
                        <span>Subscription</span>
                    </Link>

                    {/* User Info */}
                    <div className="flex items-center gap-2 px-3 py-1.5 rounded-full bg-slate-800 border border-slate-700">
                        <User size={14} className="text-primary" />
                        <span className="text-sm font-medium text-slate-300 capitalize">{username || "Student"}</span>
                    </div>
                    <button
                        onClick={handleLogout}
                        className="p-2 text-slate-400 hover:text-white hover:bg-slate-800 rounded-lg transition-colors"
                    >
                        <LogOut size={20} />
                    </button>
                </div>
            </div>
        </nav>
    );
}
