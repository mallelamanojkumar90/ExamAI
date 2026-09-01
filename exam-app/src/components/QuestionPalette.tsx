"use client";

import { CheckCircle, Circle, Flag } from "lucide-react";

interface QuestionStatus {
  answered: boolean;
  markedForReview: boolean;
}

interface QuestionPaletteProps {
  totalQuestions: number;
  currentQuestion: number;
  statuses: Record<number, QuestionStatus>;
  onQuestionSelect: (index: number) => void;
}

export function QuestionPalette({
  totalQuestions,
  currentQuestion,
  statuses,
  onQuestionSelect,
}: QuestionPaletteProps) {
  const getQuestionStyle = (index: number) => {
    const status = statuses[index] || { answered: false, markedForReview: false };
    
    // 🟣 Answered & Marked for Review
    if (status.answered && status.markedForReview) {
      return "bg-purple-500 text-white border-purple-400";
    }
    // ✅ Answered
    if (status.answered) {
      return "bg-green-500 text-white border-green-400";
    }
    // 🚩 Marked for Review
    if (status.markedForReview) {
      return "bg-yellow-500 text-white border-yellow-400";
    }
    // ⭕ Not Answered
    return "bg-slate-700 text-slate-300 border-slate-600";
  };

  const getIcon = (index: number) => {
    const status = statuses[index] || { answered: false, markedForReview: false };
    
    if (status.answered && status.markedForReview) {
      return <Flag size={10} className="absolute -top-1 -right-1" />;
    }
    if (status.answered) {
      return <CheckCircle size={10} className="absolute -top-1 -right-1" />;
    }
    if (status.markedForReview) {
      return <Flag size={10} className="absolute -top-1 -right-1" />;
    }
    return null;
  };

  // Calculate statistics
  const answeredCount = Object.values(statuses).filter(s => s.answered).length;
  const markedCount = Object.values(statuses).filter(s => s.markedForReview).length;
  const notAnsweredCount = totalQuestions - answeredCount;
  const notVisitedCount = totalQuestions - Object.keys(statuses).length;

  return (
    <div className="glass-panel p-4">
      <h3 className="text-lg font-semibold mb-4">Question Palette</h3>
      
      {/* Legend */}
      <div className="grid grid-cols-2 gap-2 mb-4 text-xs">
        <div className="flex items-center gap-2">
          <div className="w-5 h-5 bg-green-500 rounded border border-green-400"></div>
          <span className="text-slate-300">Answered</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-5 h-5 bg-slate-700 rounded border border-slate-600"></div>
          <span className="text-slate-300">Not Answered</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-5 h-5 bg-yellow-500 rounded border border-yellow-400"></div>
          <span className="text-slate-300">Marked</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-5 h-5 bg-purple-500 rounded border border-purple-400"></div>
          <span className="text-slate-300">Ans + Marked</span>
        </div>
      </div>

      {/* Question Grid */}
      <div className="grid grid-cols-5 gap-2 mb-4 max-h-96 overflow-y-auto pr-2">
        {Array.from({ length: totalQuestions }).map((_, index) => (
          <button
            key={index}
            onClick={() => onQuestionSelect(index)}
            className={`
              relative w-full aspect-square rounded-lg border-2 
              flex items-center justify-center
              transition-all hover:scale-110 hover:shadow-lg
              ${getQuestionStyle(index)}
              ${currentQuestion === index ? "ring-2 ring-white ring-offset-2 ring-offset-slate-900 scale-110" : ""}
            `}
            title={`Question ${index + 1}`}
          >
            <span className="text-xs font-bold">{index + 1}</span>
            {getIcon(index)}
          </button>
        ))}
      </div>

      {/* Statistics */}
      <div className="pt-4 border-t border-slate-700">
        <div className="grid grid-cols-2 gap-3 text-sm">
          <div className="flex justify-between">
            <span className="text-slate-400">Answered:</span>
            <span className="font-semibold text-green-400">{answeredCount}</span>
          </div>
          <div className="flex justify-between">
            <span className="text-slate-400">Not Answered:</span>
            <span className="font-semibold text-slate-300">{notAnsweredCount}</span>
          </div>
          <div className="flex justify-between">
            <span className="text-slate-400">Marked:</span>
            <span className="font-semibold text-yellow-400">{markedCount}</span>
          </div>
          <div className="flex justify-between">
            <span className="text-slate-400">Not Visited:</span>
            <span className="font-semibold text-slate-500">{notVisitedCount}</span>
          </div>
        </div>
      </div>
    </div>
  );
}
