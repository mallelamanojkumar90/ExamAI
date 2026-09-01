"use client";

import { useState, useEffect, Fragment } from "react";
import Navbar from "@/components/Navbar";
import { User, Calendar, Award, Clock, ChevronDown, ChevronUp, Search } from "lucide-react";

interface UserData {
    username: string;
    full_name: string;
    last_active: string | null;
    exams_taken: number;
}

interface ExamActivity {
    id: number;
    subject: string;
    difficulty: string;
    score: number;
    total_questions: number;
    timestamp: string;
}

export default function StudentsPage() {
    const [users, setUsers] = useState<UserData[]>([]);
    const [loading, setLoading] = useState(true);
    const [expandedUser, setExpandedUser] = useState<string | null>(null);
    const [activityData, setActivityData] = useState<Record<string, ExamActivity[]>>({});
    const [loadingActivity, setLoadingActivity] = useState<string | null>(null);
    const [searchTerm, setSearchTerm] = useState("");

    useEffect(() => {
        fetchUsers();
    }, []);

    const fetchUsers = async () => {
        try {
            const res = await fetch("http://localhost:8000/admin/users");
            if (res.ok) {
                const data = await res.json();
                setUsers(data);
            }
        } catch (error) {
            console.error("Failed to fetch users", error);
        } finally {
            setLoading(false);
        }
    };

    const fetchUserActivity = async (username: string) => {
        if (activityData[username]) return; // Already fetched

        setLoadingActivity(username);
        try {
            const res = await fetch(`http://localhost:8000/admin/user/${username}/activity`);
            if (res.ok) {
                const data = await res.json();
                setActivityData(prev => ({ ...prev, [username]: data }));
            }
        } catch (error) {
            console.error("Failed to fetch activity", error);
        } finally {
            setLoadingActivity(null);
        }
    };

    const toggleUser = (username: string) => {
        if (expandedUser === username) {
            setExpandedUser(null);
        } else {
            setExpandedUser(username);
            fetchUserActivity(username);
        }
    };

    const filteredUsers = users.filter(user =>
        user.username.toLowerCase().includes(searchTerm.toLowerCase()) ||
        (user.full_name && user.full_name.toLowerCase().includes(searchTerm.toLowerCase()))
    );

    return (
        <div className="min-h-screen bg-slate-950 text-slate-200 font-sans selection:bg-primary/30">
            <Navbar />

            <main className="container mx-auto px-4 py-8 max-w-6xl">
                <div className="flex items-center justify-between mb-8">
                    <div>
                        <h1 className="text-3xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-white to-slate-400">
                            Student Management
                        </h1>
                        <p className="text-slate-400 mt-2">View registered students and their exam activity</p>
                    </div>
                </div>

                {/* Search Bar */}
                <div className="mb-6 relative">
                    <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                        <Search className="h-5 w-5 text-slate-500" />
                    </div>
                    <input
                        type="text"
                        placeholder="Search students by username or name..."
                        className="w-full pl-10 pr-4 py-3 bg-slate-900/50 border border-slate-800 rounded-xl focus:ring-2 focus:ring-primary/50 focus:border-primary/50 text-slate-200 placeholder-slate-500 transition-all"
                        value={searchTerm}
                        onChange={(e) => setSearchTerm(e.target.value)}
                    />
                </div>

                {loading ? (
                    <div className="flex justify-center py-12">
                        <div className="w-8 h-8 border-4 border-primary border-t-transparent rounded-full animate-spin"></div>
                    </div>
                ) : (
                    <div className="bg-slate-900/50 border border-slate-800 rounded-2xl overflow-hidden backdrop-blur-sm">
                        <div className="overflow-x-auto">
                            <table className="w-full">
                                <thead>
                                    <tr className="bg-slate-900 border-b border-slate-800">
                                        <th className="px-6 py-4 text-left text-sm font-semibold text-slate-400">Student</th>
                                        <th className="px-6 py-4 text-left text-sm font-semibold text-slate-400">Full Name</th>
                                        <th className="px-6 py-4 text-left text-sm font-semibold text-slate-400">Exams Taken</th>
                                        <th className="px-6 py-4 text-left text-sm font-semibold text-slate-400">Last Active</th>
                                        <th className="px-6 py-4 text-right text-sm font-semibold text-slate-400">Actions</th>
                                    </tr>
                                </thead>
                                <tbody className="divide-y divide-slate-800">
                                    {filteredUsers.length === 0 ? (
                                        <tr>
                                            <td colSpan={5} className="px-6 py-8 text-center text-slate-500">
                                                No students found matching your search.
                                            </td>
                                        </tr>
                                    ) : (
                                        filteredUsers.map((user) => (
                                            <Fragment key={user.username}>
                                                <tr
                                                    className={`hover:bg-slate-800/50 transition-colors cursor-pointer ${expandedUser === user.username ? 'bg-slate-800/30' : ''}`}
                                                    onClick={() => toggleUser(user.username)}
                                                >
                                                    <td className="px-6 py-4">
                                                        <div className="flex items-center gap-3">
                                                            <div className="w-8 h-8 rounded-full bg-primary/10 flex items-center justify-center text-primary">
                                                                <User size={16} />
                                                            </div>
                                                            <span className="font-medium text-slate-200">{user.username}</span>
                                                        </div>
                                                    </td>
                                                    <td className="px-6 py-4 text-slate-400">{user.full_name || "-"}</td>
                                                    <td className="px-6 py-4">
                                                        <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-500/10 text-blue-400 border border-blue-500/20">
                                                            {user.exams_taken} exams
                                                        </span>
                                                    </td>
                                                    <td className="px-6 py-4 text-slate-400 text-sm">
                                                        {user.last_active ? new Date(user.last_active).toLocaleDateString() : "Never"}
                                                    </td>
                                                    <td className="px-6 py-4 text-right">
                                                        <button
                                                            className="text-slate-400 hover:text-white transition-colors"
                                                            onClick={(e) => {
                                                                e.stopPropagation();
                                                                toggleUser(user.username);
                                                            }}
                                                        >
                                                            {expandedUser === user.username ? <ChevronUp size={20} /> : <ChevronDown size={20} />}
                                                        </button>
                                                    </td>
                                                </tr>
                                                {expandedUser === user.username && (
                                                    <tr className="bg-slate-900/30">
                                                        <td colSpan={5} className="px-6 py-6">
                                                            <div className="pl-11">
                                                                <h3 className="text-sm font-semibold text-slate-300 mb-4 flex items-center gap-2">
                                                                    <Award size={16} className="text-primary" />
                                                                    Exam History
                                                                </h3>

                                                                {loadingActivity === user.username ? (
                                                                    <div className="flex items-center gap-2 text-slate-500 text-sm">
                                                                        <div className="w-4 h-4 border-2 border-slate-500 border-t-transparent rounded-full animate-spin"></div>
                                                                        Loading activity...
                                                                    </div>
                                                                ) : !activityData[user.username] || activityData[user.username].length === 0 ? (
                                                                    <p className="text-slate-500 text-sm italic">No exams taken yet.</p>
                                                                ) : (
                                                                    <div className="grid gap-3">
                                                                        {activityData[user.username].map((exam) => (
                                                                            <div key={exam.id} className="bg-slate-950 border border-slate-800 rounded-lg p-4 flex items-center justify-between">
                                                                                <div className="flex items-center gap-4">
                                                                                    <div className={`w-10 h-10 rounded-lg flex items-center justify-center font-bold text-lg
                                                                                        ${exam.score / exam.total_questions >= 0.7 ? 'bg-green-500/10 text-green-500 border border-green-500/20' :
                                                                                            exam.score / exam.total_questions >= 0.4 ? 'bg-yellow-500/10 text-yellow-500 border border-yellow-500/20' :
                                                                                                'bg-red-500/10 text-red-500 border border-red-500/20'}`}
                                                                                    >
                                                                                        {Math.round((exam.score / exam.total_questions) * 100)}%
                                                                                    </div>
                                                                                    <div>
                                                                                        <h4 className="font-medium text-slate-200">{exam.subject}</h4>
                                                                                        <div className="flex items-center gap-3 text-xs text-slate-500 mt-1">
                                                                                            <span className="flex items-center gap-1">
                                                                                                <Award size={12} />
                                                                                                {exam.difficulty}
                                                                                            </span>
                                                                                            <span className="flex items-center gap-1">
                                                                                                <Clock size={12} />
                                                                                                {new Date(exam.timestamp).toLocaleString()}
                                                                                            </span>
                                                                                        </div>
                                                                                    </div>
                                                                                </div>
                                                                                <div className="text-right">
                                                                                    <div className="text-xl font-bold text-white">
                                                                                        {exam.score}<span className="text-slate-500 text-sm font-normal">/{exam.total_questions}</span>
                                                                                    </div>
                                                                                    <div className="text-xs text-slate-500">Score</div>
                                                                                </div>
                                                                            </div>
                                                                        ))}
                                                                    </div>
                                                                )}
                                                            </div>
                                                        </td>
                                                    </tr>
                                                )}
                                            </Fragment>
                                        ))
                                    )}
                                </tbody>
                            </table>
                        </div>
                    </div>
                )}
            </main>
        </div>
    );
}
