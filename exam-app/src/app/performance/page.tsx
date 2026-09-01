"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import {
  TrendingUp,
  TrendingDown,
  Minus,
  Trophy,
  Target,
  Clock,
  BookOpen,
  Award,
  BarChart3,
  Activity,
  ChevronRight,
} from "lucide-react";

interface PerformanceSummary {
  total_exams: number;
  average_score: number;
  total_questions: number;
  correct_answers: number;
  accuracy: number;
  recent_trend: "improving" | "declining" | "stable" | "neutral";
  subjects_performance: Record<string, SubjectPerformance>;
  difficulty_performance: Record<string, DifficultyPerformance>;
  time_spent_minutes: number;
}

interface SubjectPerformance {
  attempts: number;
  total_questions: number;
  correct_answers: number;
  accuracy: number;
}

interface DifficultyPerformance {
  attempts: number;
  total_questions: number;
  correct_answers: number;
  accuracy: number;
}

interface PeerComparison {
  user_accuracy: number;
  peer_average: number;
  percentile: number;
  rank: number;
  total_users: number;
}

interface Analysis {
  strengths: Array<{ subject: string; accuracy: number; attempts: number }>;
  weaknesses: Array<{ subject: string; accuracy: number; attempts: number }>;
  recommendations: string[];
}

interface TimelineData {
  date: string;
  exams: number;
  total_questions: number;
  correct_answers: number;
  accuracy: number;
}

interface RecentActivity {
  attempt_id: number;
  exam_name: string;
  subject: string;
  score: number;
  total_questions: number;
  accuracy: number;
  started_at: string;
  completed_at: string;
  time_taken_minutes: number;
}

export default function PerformanceDashboard() {
  const router = useRouter();
  const [loading, setLoading] = useState(true);
  const [userId, setUserId] = useState<number | null>(null);
  const [summary, setSummary] = useState<PerformanceSummary | null>(null);
  const [peerComparison, setPeerComparison] = useState<PeerComparison | null>(
    null
  );
  const [analysis, setAnalysis] = useState<Analysis | null>(null);
  const [timeline, setTimeline] = useState<TimelineData[]>([]);
  const [recentActivity, setRecentActivity] = useState<RecentActivity[]>([]);

  useEffect(() => {
    const userStr = localStorage.getItem("user");
    if (!userStr) {
      router.push("/");
      return;
    }

    try {
      // Check if userStr is a JSON string or just a username
      let userId = 1; // Default fallback
      
      if (userStr.startsWith("{")) {
        const userData = JSON.parse(userStr);
        if (userData && userData.user_id) {
          userId = userData.user_id;
        } else {
          // If JSON but no user_id (shouldn't happen with new login)
          console.warn("No user_id found in local storage");
          router.push("/");
          return;
        }
      } else {
        // Legacy format (just username string)
        alert("Please login again to access performance features.");
        localStorage.removeItem("user");
        router.push("/");
        return;
      }

      setUserId(userId);
      fetchDashboardData(userId);
    } catch (error) {
      console.error("Error parsing user data:", error);
      router.push("/");
    }
  }, []);

  const fetchDashboardData = async (userId: number) => {
    try {
      const response = await fetch(
        `http://localhost:8000/api/performance/dashboard/${userId}`
      );
      const data = await response.json();

      if (data.success) {
        setSummary(data.dashboard.summary);
        setPeerComparison(data.dashboard.peer_comparison);
        setAnalysis(data.dashboard.analysis);
        setTimeline(data.dashboard.timeline);
        setRecentActivity(data.dashboard.recent_activity);
      }
    } catch (error) {
      console.error("Error fetching dashboard data:", error);
    } finally {
      setLoading(false);
    }
  };

  const getTrendIcon = (trend: string) => {
    switch (trend) {
      case "improving":
        return <TrendingUp className="w-5 h-5 text-green-400" />;
      case "declining":
        return <TrendingDown className="w-5 h-5 text-red-400" />;
      case "stable":
        return <Minus className="w-5 h-5 text-yellow-400" />;
      default:
        return <Minus className="w-5 h-5 text-gray-400" />;
    }
  };

  const getTrendColor = (trend: string) => {
    switch (trend) {
      case "improving":
        return "text-green-400";
      case "declining":
        return "text-red-400";
      case "stable":
        return "text-yellow-400";
      default:
        return "text-gray-400";
    }
  };

  const getAccuracyColor = (accuracy: number) => {
    if (accuracy >= 80) return "text-green-400";
    if (accuracy >= 60) return "text-yellow-400";
    return "text-red-400";
  };

  const getAccuracyBgColor = (accuracy: number) => {
    if (accuracy >= 80) return "bg-green-500/20";
    if (accuracy >= 60) return "bg-yellow-500/20";
    return "bg-red-500/20";
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 flex items-center justify-center">
        <div className="text-white text-xl">Loading performance data...</div>
      </div>
    );
  }

  if (!summary) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 flex items-center justify-center">
        <div className="text-center">
          <div className="text-white text-xl mb-4">No performance data yet</div>
          <p className="text-gray-400 mb-6">
            Take some exams to see your performance analytics
          </p>
          <button
            onClick={() => router.push("/dashboard")}
            className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
          >
            Go to Dashboard
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 py-8 px-4 sm:px-6 lg:px-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <button
            onClick={() => router.push("/dashboard")}
            className="text-gray-400 hover:text-white mb-4 flex items-center gap-2 transition-colors"
          >
            ← Back to Dashboard
          </button>
          <h1 className="text-4xl font-bold text-white mb-2">
            Performance Analytics
          </h1>
          <p className="text-gray-400">
            Track your progress and identify areas for improvement
          </p>
        </div>

        {/* Key Metrics */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          {/* Total Exams */}
          <div className="bg-white/5 backdrop-blur-lg rounded-xl p-6 border border-gray-700 hover:border-blue-500 transition-all">
            <div className="flex items-center justify-between mb-4">
              <BookOpen className="w-8 h-8 text-blue-400" />
              <div className={getTrendColor(summary.recent_trend)}>
                {getTrendIcon(summary.recent_trend)}
              </div>
            </div>
            <div className="text-3xl font-bold text-white mb-1">
              {summary.total_exams}
            </div>
            <div className="text-gray-400 text-sm">Total Exams</div>
          </div>

          {/* Average Accuracy */}
          <div className="bg-white/5 backdrop-blur-lg rounded-xl p-6 border border-gray-700 hover:border-green-500 transition-all">
            <div className="flex items-center justify-between mb-4">
              <Target className="w-8 h-8 text-green-400" />
              <Trophy className="w-6 h-6 text-yellow-400" />
            </div>
            <div className={`text-3xl font-bold mb-1 ${getAccuracyColor(summary.accuracy)}`}>
              {summary.accuracy.toFixed(1)}%
            </div>
            <div className="text-gray-400 text-sm">Overall Accuracy</div>
          </div>

          {/* Questions Attempted */}
          <div className="bg-white/5 backdrop-blur-lg rounded-xl p-6 border border-gray-700 hover:border-purple-500 transition-all">
            <div className="flex items-center justify-between mb-4">
              <Activity className="w-8 h-8 text-purple-400" />
              <BarChart3 className="w-6 h-6 text-purple-400" />
            </div>
            <div className="text-3xl font-bold text-white mb-1">
              {summary.total_questions}
            </div>
            <div className="text-gray-400 text-sm">Questions Attempted</div>
          </div>

          {/* Time Spent */}
          <div className="bg-white/5 backdrop-blur-lg rounded-xl p-6 border border-gray-700 hover:border-orange-500 transition-all">
            <div className="flex items-center justify-between mb-4">
              <Clock className="w-8 h-8 text-orange-400" />
              <Award className="w-6 h-6 text-orange-400" />
            </div>
            <div className="text-3xl font-bold text-white mb-1">
              {Math.round(summary.time_spent_minutes)}
            </div>
            <div className="text-gray-400 text-sm">Minutes Practiced</div>
          </div>
        </div>

        {/* Peer Comparison & Trend */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          {/* Peer Comparison */}
          {peerComparison && (
            <div className="bg-white/5 backdrop-blur-lg rounded-xl p-6 border border-gray-700">
              <h2 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
                <Trophy className="w-6 h-6 text-yellow-400" />
                Peer Comparison
              </h2>
              <div className="space-y-4">
                <div className="flex justify-between items-center">
                  <span className="text-gray-400">Your Accuracy</span>
                  <span className={`text-2xl font-bold ${getAccuracyColor(peerComparison.user_accuracy)}`}>
                    {peerComparison.user_accuracy.toFixed(1)}%
                  </span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-gray-400">Peer Average</span>
                  <span className="text-2xl font-bold text-white">
                    {peerComparison.peer_average.toFixed(1)}%
                  </span>
                </div>
                <div className="border-t border-gray-700 pt-4">
                  <div className="flex justify-between items-center mb-2">
                    <span className="text-gray-400">Your Rank</span>
                    <span className="text-xl font-bold text-blue-400">
                      #{peerComparison.rank} / {peerComparison.total_users}
                    </span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-gray-400">Percentile</span>
                    <span className="text-xl font-bold text-green-400">
                      Top {(100 - peerComparison.percentile).toFixed(0)}%
                    </span>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Performance Trend */}
          <div className="bg-white/5 backdrop-blur-lg rounded-xl p-6 border border-gray-700">
            <h2 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
              <TrendingUp className="w-6 h-6 text-blue-400" />
              Recent Trend
            </h2>
            <div className="flex items-center justify-center h-32">
              <div className="text-center">
                <div className={`text-6xl mb-2 ${getTrendColor(summary.recent_trend)}`}>
                  {getTrendIcon(summary.recent_trend)}
                </div>
                <div className={`text-2xl font-bold capitalize ${getTrendColor(summary.recent_trend)}`}>
                  {summary.recent_trend}
                </div>
                <p className="text-gray-400 mt-2">
                  Based on last 10 exams
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* Subject Performance */}
        <div className="bg-white/5 backdrop-blur-lg rounded-xl p-6 border border-gray-700 mb-8">
          <h2 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
            <BookOpen className="w-6 h-6 text-purple-400" />
            Subject-wise Performance
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {Object.entries(summary.subjects_performance).map(
              ([subject, data]) => (
                <div
                  key={subject}
                  className={`p-4 rounded-lg border ${getAccuracyBgColor(data.accuracy)} border-gray-600`}
                >
                  <div className="flex justify-between items-center mb-2">
                    <h3 className="text-white font-semibold">{subject}</h3>
                    <span className={`text-xl font-bold ${getAccuracyColor(data.accuracy)}`}>
                      {data.accuracy.toFixed(1)}%
                    </span>
                  </div>
                  <div className="text-sm text-gray-400">
                    {data.attempts} exams • {data.correct_answers}/
                    {data.total_questions} correct
                  </div>
                  {/* Progress bar */}
                  <div className="mt-2 bg-gray-700 rounded-full h-2">
                    <div
                      className={`h-2 rounded-full ${
                        data.accuracy >= 80
                          ? "bg-green-500"
                          : data.accuracy >= 60
                          ? "bg-yellow-500"
                          : "bg-red-500"
                      }`}
                      style={{ width: `${data.accuracy}%` }}
                    />
                  </div>
                </div>
              )
            )}
          </div>
        </div>

        {/* Strengths & Weaknesses */}
        {analysis && (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
            {/* Strengths */}
            <div className="bg-white/5 backdrop-blur-lg rounded-xl p-6 border border-green-700/50">
              <h2 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
                <Award className="w-6 h-6 text-green-400" />
                Your Strengths
              </h2>
              {analysis.strengths.length > 0 ? (
                <div className="space-y-3">
                  {analysis.strengths.map((strength, index) => (
                    <div
                      key={index}
                      className="flex items-center justify-between p-3 bg-green-500/10 rounded-lg"
                    >
                      <span className="text-white font-medium">
                        {strength.subject}
                      </span>
                      <span className="text-green-400 font-bold">
                        {strength.accuracy.toFixed(1)}%
                      </span>
                    </div>
                  ))}
                </div>
              ) : (
                <p className="text-gray-400">
                  Keep practicing to identify your strengths!
                </p>
              )}
            </div>

            {/* Weaknesses */}
            <div className="bg-white/5 backdrop-blur-lg rounded-xl p-6 border border-red-700/50">
              <h2 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
                <Target className="w-6 h-6 text-red-400" />
                Areas to Improve
              </h2>
              {analysis.weaknesses.length > 0 ? (
                <div className="space-y-3">
                  {analysis.weaknesses.map((weakness, index) => (
                    <div
                      key={index}
                      className="flex items-center justify-between p-3 bg-red-500/10 rounded-lg"
                    >
                      <span className="text-white font-medium">
                        {weakness.subject}
                      </span>
                      <span className="text-red-400 font-bold">
                        {weakness.accuracy.toFixed(1)}%
                      </span>
                    </div>
                  ))}
                </div>
              ) : (
                <p className="text-gray-400">
                  Great job! No weak areas identified.
                </p>
              )}
            </div>
          </div>
        )}

        {/* Recommendations */}
        {analysis && analysis.recommendations.length > 0 && (
          <div className="bg-white/5 backdrop-blur-lg rounded-xl p-6 border border-blue-700/50 mb-8">
            <h2 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
              <Activity className="w-6 h-6 text-blue-400" />
              Recommendations
            </h2>
            <ul className="space-y-2">
              {analysis.recommendations.map((recommendation, index) => (
                <li
                  key={index}
                  className="flex items-start gap-3 text-gray-300"
                >
                  <ChevronRight className="w-5 h-5 text-blue-400 flex-shrink-0 mt-0.5" />
                  <span>{recommendation}</span>
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* Recent Activity */}
        {recentActivity.length > 0 && (
          <div className="bg-white/5 backdrop-blur-lg rounded-xl p-6 border border-gray-700">
            <h2 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
              <Clock className="w-6 h-6 text-orange-400" />
              Recent Activity
            </h2>
            <div className="space-y-3">
              {recentActivity.map((activity) => (
                <div
                  key={activity.attempt_id}
                  className="flex items-center justify-between p-4 bg-white/5 rounded-lg hover:bg-white/10 transition-colors"
                >
                  <div className="flex-1">
                    <div className="text-white font-medium mb-1">
                      {activity.subject}
                    </div>
                    <div className="text-sm text-gray-400">
                      {activity.score}/{activity.total_questions} correct •{" "}
                      {activity.time_taken_minutes.toFixed(0)} min
                    </div>
                  </div>
                  <div className="text-right">
                    <div className={`text-xl font-bold ${getAccuracyColor(activity.accuracy)}`}>
                      {activity.accuracy.toFixed(1)}%
                    </div>
                    <div className="text-xs text-gray-500">
                      {new Date(activity.started_at).toLocaleDateString()}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
