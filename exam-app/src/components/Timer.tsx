"use client";

import { useEffect, useState } from "react";
import { Clock } from "lucide-react";

interface TimerProps {
    durationInSeconds: number;
    onTimeUp: () => void;
}

export default function Timer({ durationInSeconds, onTimeUp }: TimerProps) {
    const [timeLeft, setTimeLeft] = useState(durationInSeconds);

    useEffect(() => {
        if (timeLeft <= 0) {
            onTimeUp();
            return;
        }

        const interval = setInterval(() => {
            setTimeLeft((prev) => prev - 1);
        }, 1000);

        return () => clearInterval(interval);
    }, [timeLeft, onTimeUp]);

    const formatTime = (seconds: number) => {
        const mins = Math.floor(seconds / 60);
        const secs = seconds % 60;
        return `${mins.toString().padStart(2, "0")}:${secs.toString().padStart(2, "0")}`;
    };

    return (
        <div className={`flex items-center gap-2 px-4 py-2 rounded-full border ${timeLeft < 60 ? "bg-red-500/10 border-red-500/50 text-red-400" : "bg-slate-800 border-slate-700 text-slate-300"
            }`}>
            <Clock size={16} className={timeLeft < 60 ? "animate-pulse" : ""} />
            <span className="font-mono font-semibold text-lg">{formatTime(timeLeft)}</span>
        </div>
    );
}
