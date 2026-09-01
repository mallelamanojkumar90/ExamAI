"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { useSession } from "next-auth/react";
import { motion } from "framer-motion";
import { 
    Calculator, Atom, FlaskConical, Dna, Layers, Play, Clock, 
    CheckCircle, BookOpen, GraduationCap, Stethoscope, Microscope 
} from "lucide-react";
import Navbar from "@/components/Navbar";

// Exam type configurations
const examTypes = [
    {
        id: "IIT_JEE",
        name: "IIT/JEE",
        fullName: "Joint Entrance Examination",
        icon: GraduationCap,
        color: "from-blue-500 to-cyan-500",
        description: "Engineering entrance for IITs, NITs",
        subjects: ["Physics", "Chemistry", "Mathematics"],
        totalQuestions: 90,
        questionsPerSubject: 30,
        duration: 180 // minutes
    },
    {
        id: "NEET",
        name: "NEET",
        fullName: "National Eligibility cum Entrance Test",
        icon: Stethoscope,
        color: "from-green-500 to-emerald-500",
        description: "Medical entrance for MBBS, BDS",
        subjects: ["Physics", "Chemistry", "Biology"],
        totalQuestions: 180,
        questionsPerSubject: 45,
        duration: 180 // minutes
    },
    {
        id: "EAMCET",
        name: "EAMCET",
        fullName: "Engineering, Agriculture and Medical CET",
        icon: Microscope,
        color: "from-purple-500 to-pink-500",
        description: "State-level entrance exam",
        subjects: ["Physics", "Chemistry", "Mathematics", "Biology"],
        totalQuestions: 160,
        questionsPerSubject: 40,
        duration: 180 // minutes
    }
];

// Subject icons mapping
const subjectIcons: Record<string, any> = {
    "Physics": Atom,
    "Chemistry": FlaskConical,
    "Mathematics": Calculator,
    "Biology": Dna
};

const difficulties = ["Easy", "Medium", "Hard"];

export default function Dashboard() {
    const router = useRouter();
    const { data: session } = useSession();
    const [selectedExamType, setSelectedExamType] = useState<string | null>(null);
    const [selectedSubject, setSelectedSubject] = useState<string | null>(null);
    const [difficulty, setDifficulty] = useState("Medium");
    const [questionCount, setQuestionCount] = useState(10);
    const [availableSubjects, setAvailableSubjects] = useState<string[]>([]);
    const [username, setUsername] = useState<string>("Student");

    // Load username from NextAuth session or localStorage
    useEffect(() => {
        // First, try to get from NextAuth session (for Google OAuth users)
        if (session?.user?.name) {
            setUsername(session.user.name);
        } else if (session?.user?.email) {
            // Fallback to email if name is not available
            setUsername(session.user.email);
        } else {
            // Fallback to localStorage (for traditional email/password login)
            const storedUser = localStorage.getItem("user");
            if (storedUser) {
                try {
                    if (storedUser.startsWith("{")) {
                        const userData = JSON.parse(storedUser);
                        // Use full_name if available, fallback to username (email), then "Student"
                        setUsername(userData.full_name || userData.username || "Student");
                    } else {
                        setUsername(storedUser);
                    }
                } catch (e) {
                    console.error("Error parsing user data", e);
                    setUsername("Student");
                }
            }
        }
    }, [session]);

    // Update available subjects when exam type changes
    useEffect(() => {
        if (selectedExamType) {
            const examType = examTypes.find(e => e.id === selectedExamType);
            if (examType) {
                setAvailableSubjects(examType.subjects);
                setSelectedSubject(null); // Reset subject selection
            }
        } else {
            setAvailableSubjects([]);
            setSelectedSubject(null);
        }
    }, [selectedExamType]);

    const startExam = () => {
        if (!selectedExamType) {
            alert("Please select an exam type");
            return;
        }
        
        // All exam types now use fixed configuration (no subject/count selection)
        router.push(`/exam?examType=${selectedExamType}&difficulty=${difficulty}`);
    };

    const selectedExamTypeData = examTypes.find(e => e.id === selectedExamType);

    return (
        <div className="min-h-screen bg-background">
            <Navbar />

            <main className="container py-12">
                <div className="mb-12">
                    <h1 className="text-3xl font-bold mb-2">Welcome back, {username}</h1>
                    <p className="text-slate-400">Choose your exam type and configure your practice test.</p>
                </div>

                <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                    {/* Configuration Panel */}
                    <div className="lg:col-span-2 space-y-8">
                        {/* Exam Type Selection */}
                        <section>
                            <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
                                <BookOpen className="text-primary" size={20} />
                                Select Exam Type
                            </h2>
                            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                                {examTypes.map((examType) => (
                                    <motion.button
                                        key={examType.id}
                                        whileHover={{ scale: 1.02 }}
                                        whileTap={{ scale: 0.98 }}
                                        onClick={() => setSelectedExamType(examType.id)}
                                        className={`relative p-6 rounded-xl border text-left transition-all overflow-hidden group ${
                                            selectedExamType === examType.id
                                                ? "border-primary bg-primary/10 ring-1 ring-primary"
                                                : "border-slate-800 bg-slate-900/50 hover:border-slate-700"
                                        }`}
                                    >
                                        <div className={`absolute top-0 right-0 w-24 h-24 bg-gradient-to-br ${examType.color} opacity-10 rounded-bl-full -mr-4 -mt-4 transition-opacity group-hover:opacity-20`} />
                                        <examType.icon className={`w-8 h-8 mb-4 ${selectedExamType === examType.id ? "text-primary" : "text-slate-400"}`} />
                                        <h3 className="font-semibold text-lg">{examType.name}</h3>
                                        <p className="text-xs text-slate-500 mt-1">{examType.description}</p>

                                        {selectedExamType === examType.id && (
                                            <div className="absolute top-4 right-4 text-primary">
                                                <CheckCircle size={20} />
                                            </div>
                                        )}
                                    </motion.button>
                                ))}
                            </div>
                        </section>

                        {/* Subject Selection removed - all exam types have fixed configurations */}

                        {/* Exam Settings - Show after exam type selection */}
                        {selectedExamType && (
                            <motion.section
                                initial={{ opacity: 0, y: 20 }}
                                animate={{ opacity: 1, y: 0 }}
                                transition={{ duration: 0.3 }}
                            >
                                <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
                                    <Clock className="text-primary" size={20} />
                                    Exam Settings
                                </h2>
                                <div className="glass-panel p-6 space-y-6">
                                    {/* Difficulty Level - Always shown */}
                                    <div>
                                        <label className="block text-sm font-medium text-slate-400 mb-3">Difficulty Level</label>
                                        <div className="flex gap-2">
                                            {difficulties.map((level) => (
                                                <button
                                                    key={level}
                                                    onClick={() => setDifficulty(level)}
                                                    className={`flex-1 py-2 px-4 rounded-lg text-sm font-medium border transition-all ${
                                                        difficulty === level
                                                            ? "bg-primary text-primary-foreground border-primary"
                                                            : "bg-slate-800 border-slate-700 text-slate-400 hover:bg-slate-700"
                                                    }`}
                                                >
                                                    {level}
                                                </button>
                                            ))}
                                        </div>
                                    </div>

                                    {/* Exam Configuration Info - Show for all exam types */}
                                    {selectedExamTypeData && (
                                        <div className="p-4 bg-blue-500/10 border border-blue-500/20 rounded-lg">
                                            <h3 className="text-sm font-semibold text-blue-400 mb-3">
                                                {selectedExamTypeData.name} Exam Configuration
                                            </h3>
                                            <div className="space-y-2 text-sm">
                                                <div className="flex justify-between">
                                                    <span className="text-slate-400">Total Questions:</span>
                                                    <span className="text-white font-medium">
                                                        {selectedExamTypeData.totalQuestions} questions
                                                    </span>
                                                </div>
                                                {selectedExamTypeData.subjects.map((subj: string) => (
                                                    <div key={subj} className="flex justify-between">
                                                        <span className="text-slate-400">{subj}:</span>
                                                        <span className="text-white font-medium">
                                                            {selectedExamTypeData.questionsPerSubject} questions
                                                        </span>
                                                    </div>
                                                ))}
                                                <div className="flex justify-between pt-2 border-t border-blue-500/20">
                                                    <span className="text-slate-400">Duration:</span>
                                                    <span className="text-white font-medium">
                                                        {selectedExamTypeData.duration} minutes ({Math.floor(selectedExamTypeData.duration / 60)} hours)
                                                    </span>
                                                </div>
                                            </div>
                                        </div>
                                    )}
                                </div>
                            </motion.section>
                        )}
                    </div>

                    {/* Summary Card */}
                    <div className="lg:col-span-1">
                        <div className="sticky top-24">
                            <div className="glass-panel p-6 border-t-4 border-t-primary">
                                <h3 className="text-lg font-semibold mb-4">Exam Summary</h3>
                                <div className="space-y-4 mb-6">
                                    <div className="flex justify-between items-center pb-3 border-b border-slate-700">
                                        <span className="text-slate-400">Exam Type</span>
                                        <span className="font-medium">{selectedExamTypeData?.name || "-"}</span>
                                    </div>
                                    
                                    {/* Subjects - Show all subjects for all exam types */}
                                    {selectedExamTypeData && (
                                        <div className="flex justify-between items-center pb-3 border-b border-slate-700">
                                            <span className="text-slate-400">Subjects</span>
                                            <span className="font-medium text-sm">
                                                {selectedExamTypeData.subjects.join(", ")}
                                            </span>
                                        </div>
                                    )}
                                    
                                    <div className="flex justify-between items-center pb-3 border-b border-slate-700">
                                        <span className="text-slate-400">Difficulty</span>
                                        <span className={`font-medium px-2 py-0.5 rounded text-xs ${
                                            difficulty === "Easy" ? "bg-green-500/20 text-green-400" :
                                            difficulty === "Medium" ? "bg-yellow-500/20 text-yellow-400" :
                                                "bg-red-500/20 text-red-400"
                                        }`}>
                                            {difficulty}
                                        </span>
                                    </div>
                                    <div className="flex justify-between items-center pb-3 border-b border-slate-700">
                                        <span className="text-slate-400">Questions</span>
                                        <span className="font-medium">
                                            {selectedExamTypeData?.totalQuestions || "-"}
                                        </span>
                                    </div>
                                    <div className="flex justify-between items-center">
                                        <span className="text-slate-400">Duration</span>
                                        <span className="font-medium">
                                            {selectedExamTypeData ? `${selectedExamTypeData.duration} mins` : "-"}
                                        </span>
                                    </div>
                                </div>

                                <button
                                    onClick={startExam}
                                    disabled={!selectedExamType}
                                    className={`w-full py-4 rounded-xl font-bold text-lg transition-all shadow-lg flex items-center justify-center gap-3 ${
                                        selectedExamType
                                            ? "bg-gradient-to-r from-primary to-blue-600 text-white hover:scale-[1.02] active:scale-[0.98] hover:shadow-primary/25"
                                            : "bg-slate-800 text-slate-500 cursor-not-allowed"
                                    }`}
                                >
                                    <Play size={20} fill="currentColor" />
                                    Start Exam
                                </button>

                                {/* Info Box */}
                                {selectedExamTypeData && (
                                    <motion.div
                                        initial={{ opacity: 0, y: 10 }}
                                        animate={{ opacity: 1, y: 0 }}
                                        className="mt-4 p-4 bg-blue-500/10 border border-blue-500/20 rounded-lg"
                                    >
                                        <p className="text-xs text-blue-400 font-medium mb-1">
                                            {selectedExamTypeData.fullName}
                                        </p>
                                        <p className="text-xs text-slate-400">
                                            {selectedExamTypeData.description}
                                        </p>
                                    </motion.div>
                                )}
                            </div>
                        </div>
                    </div>
                </div>
            </main>
        </div>
    );
}
