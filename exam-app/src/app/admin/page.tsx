"use client";

import { useState, useRef, useEffect } from "react";
import Link from "next/link";
import { 
    Upload, FileText, CheckCircle, 
    AlertCircle, Loader2, User, GraduationCap, 
    BookOpen, Layers, Microscope, Atom, Stethoscope,
    RefreshCw, Database
} from "lucide-react";
import Navbar from "@/components/Navbar";

interface Document {
    id: number;
    filename: string;
    subject: string;
    topic?: string; // This will hold the exam_type
    upload_date: string;
}

interface VectorStats {
    total_vector_count: number;
    dimension: number;
    index_fullness: number;
    namespaces: Record<string, { vector_count: number }>;
}

const EXAM_TYPES = [
    { id: "IIT_JEE", name: "IIT/JEE", icon: GraduationCap, color: "text-blue-400", bg: "bg-blue-500/10", border: "border-blue-500/20" },
    { id: "NEET", name: "NEET", icon: Stethoscope, color: "text-green-400", bg: "bg-green-500/10", border: "border-green-500/20" },
    { id: "EAMCET", name: "EAMCET", icon: Microscope, color: "text-purple-400", bg: "bg-purple-500/10", border: "border-purple-500/20" },
];

export default function AdminDashboard() {
    const [files, setFiles] = useState<File[]>([]);
    const [uploading, setUploading] = useState(false);
    const [status, setStatus] = useState<{ type: "success" | "error" | null; message: string }>({
        type: null,
        message: "",
    });
    const [documents, setDocuments] = useState<Document[]>([]);
    const [loadingDocs, setLoadingDocs] = useState(true);
    const [vectorStats, setVectorStats] = useState<VectorStats | null>(null);
    const [syncing, setSyncing] = useState(false);
    
    // New States for Exam Type Grouping
    const [selectedExamType, setSelectedExamType] = useState<string>("IIT_JEE");
    const [activeTab, setActiveTab] = useState<string>("IIT_JEE");
    
    const fileInputRef = useRef<HTMLInputElement>(null);

    // Fetch document list
    const fetchDocuments = async () => {
        try {
            const res = await fetch("http://localhost:8000/documents");
            if (res.ok) {
                const data = await res.json();
                setDocuments(data);
            }
        } catch (e) {
            console.error("Failed to fetch documents", e);
        } finally {
            setLoadingDocs(false);
        }
    };

    // Sync with Pinecone and refresh documents
    const syncVectorDB = async () => {
        setSyncing(true);
        try {
            await fetchDocuments();
            const res = await fetch("http://localhost:8000/debug/index-stats");
            if (res.ok) {
                const { stats } = await res.json();
                setVectorStats(stats);
                setStatus({ type: "success", message: "Vector DB synced successfully" });
            } else {
                // If endpoint doesn't exist yet, just ignore stats
                // throw new Error("Failed to fetch vector stats");
            }
        } catch (e) {
            console.error(e);
            // Don't show error for stats failure as it might be dev environment
        } finally {
            setSyncing(false);
            setTimeout(() => setStatus({ type: null, message: "" }), 3000);
        }
    };

    // Handle file selection (multiple)
    const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.files) {
            setFiles(Array.from(e.target.files));
            setStatus({ type: null, message: "" });
        }
    };

    // Upload all selected files sequentially
    const handleUpload = async () => {
        if (files.length === 0) {
            setStatus({ type: "error", message: "Please select at least one PDF file." });
            return;
        }
        setUploading(true);
        setStatus({ type: null, message: "" });
        try {
            for (const file of files) {
                const formData = new FormData();
                formData.append("file", file);
                formData.append("exam_type", selectedExamType);
                // Subject is derived from exam_type in backend now, but we can pass it if needed.
                // The backend currently takes subject defaults to 'mixed' if not provided, 
                // but we are using exam_type to determine context.
                
                const res = await fetch("http://localhost:8000/upload-document", {
                    method: "POST",
                    body: formData,
                });
                const data = await res.json();
                if (!res.ok) {
                    throw new Error(data.detail || "Upload failed");
                }
                if (data.status === "warning") {
                    setStatus({ type: "error", message: data.message });
                } else {
                    setStatus({ type: "success", message: `Uploaded ${data.filename}` });
                }
            }
            // Clear selection after successful uploads
            setFiles([]);
            if (fileInputRef.current) fileInputRef.current.value = "";
            syncVectorDB();
        } catch (e: any) {
            console.error(e);
            setStatus({ type: "error", message: e.message || "Upload error" });
        } finally {
            setUploading(false);
        }
    };

    useEffect(() => {
        fetchDocuments();
        syncVectorDB();
    }, []);

    const managementModules = [
        {
            title: "Student Management",
            description: "Monitor registered students, view exam history and performance.",
            icon: GraduationCap,
            href: "/admin/students",
            color: "text-green-400",
            bg: "bg-green-500/10",
            border: "border-green-500/20"
        }
    ];

    // Filter documents based on active tab
    const filteredDocuments = documents.filter(doc => {
        // Fallback for older documents that might not have topic/subject formatted
        const docExamType = doc.topic || (doc.subject.includes(":") ? doc.subject.split(":")[0] : "IIT_JEE"); 
        return docExamType === activeTab || (activeTab === "IIT_JEE" && !doc.topic && !doc.subject.includes(":"));
    });

    return (
        <div className="min-h-screen bg-slate-950 text-slate-200 font-sans selection:bg-primary/30">
            <Navbar />

            <main className="container mx-auto px-4 py-8 max-w-7xl">
                {/* Header Section */}
                <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-10">
                    <div>
                        <h1 className="text-3xl font-bold text-white mb-2">Admin Dashboard</h1>
                        <p className="text-slate-400">Manage your institution's exams, content, and students</p>
                    </div>
                </div>

                {/* Management Modules Grid */}
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-12">
                    {managementModules.map((module, index) => (
                        <Link 
                            href={module.href} 
                            key={index}
                            className={`p-6 rounded-2xl border ${module.border} ${module.bg} hover:scale-[1.02] transition-transform duration-200 group`}
                        >
                            <div className="flex items-start justify-between mb-4">
                                <module.icon className={`${module.color}`} size={28} />
                                <div className={`w-8 h-8 rounded-full ${module.bg} flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity`}>
                                    <User size={14} className={module.color} />
                                </div>
                            </div>
                            <h3 className="text-xl font-bold text-white mb-2">{module.title}</h3>
                            <p className="text-slate-400 text-sm leading-relaxed">{module.description}</p>
                        </Link>
                    ))}
                </div>

                <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                    {/* Main Content Area - RAG Management */}
                    <div className="lg:col-span-2 space-y-8">
                        <div className="flex items-center justify-between">
                            <h2 className="text-2xl font-bold text-white flex items-center gap-2">
                                <BookOpen className="text-blue-400" />
                                Knowledge Base & RAG
                            </h2>
                        </div>

                        {/* Upload Section */}
                        <section className="bg-slate-900/50 border border-slate-800 rounded-2xl p-8 backdrop-blur-sm">
                            <h3 className="text-lg font-medium text-slate-300 mb-6">Upload Source Documents</h3>
                            
                            <div className="space-y-6">
                                {/* Exam Type Selector */}
                                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                                    {EXAM_TYPES.map((type) => (
                                        <button
                                            key={type.id}
                                            onClick={() => setSelectedExamType(type.id)}
                                            className={`p-4 rounded-xl border flex items-center gap-3 transition-all ${
                                                selectedExamType === type.id 
                                                ? `${type.bg} ${type.border} ring-1 ring-offset-2 ring-offset-slate-950 ring-${type.color.split('-')[1]}-500`
                                                : "bg-slate-800/50 border-slate-700 hover:bg-slate-800"
                                            }`}
                                        >
                                            <div className={`p-2 rounded-lg bg-slate-950/30`}>
                                                <type.icon size={20} className={type.color} />
                                            </div>
                                            <span className={`font-semibold ${selectedExamType === type.id ? "text-white" : "text-slate-400"}`}>
                                                {type.name}
                                            </span>
                                            {selectedExamType === type.id && (
                                                <CheckCircle size={16} className={`ml-auto ${type.color}`} />
                                            )}
                                        </button>
                                    ))}
                                </div>

                                {/* Drop Zone */}
                                <div 
                                    className={`border-2 border-dashed rounded-xl p-8 text-center transition-colors ${
                                        uploading ? "border-slate-700 bg-slate-900/30" : "border-slate-700 hover:border-blue-500/50 hover:bg-slate-800/30"
                                    }`}
                                >
                                    <input 
                                        type="file" 
                                        ref={fileInputRef}
                                        id="file-upload" 
                                        className="hidden" 
                                        accept=".pdf" 
                                        multiple 
                                        onChange={handleFileChange} 
                                    />
                                    <label htmlFor="file-upload" className="cursor-pointer block">
                                        <div className="w-14 h-14 bg-slate-800 rounded-full flex items-center justify-center mx-auto mb-4 group-hover:bg-slate-700 transition-colors">
                                            {files.length > 0 ? (
                                                <FileText className="text-blue-400" size={28} />
                                            ) : (
                                                <Upload className="text-slate-400" size={28} />
                                            )}
                                        </div>
                                        {files.length > 0 ? (
                                            <div className="space-y-1">
                                                <h3 className="text-lg font-medium text-blue-400">{files.length} file(s) selected</h3>
                                                <div className="text-sm text-slate-500">
                                                    {files.map(f => f.name).join(", ")}
                                                </div>
                                            </div>
                                        ) : (
                                            <div>
                                                <h3 className="text-lg font-medium mb-1 text-slate-200">Click to upload PDFs</h3>
                                                <p className="text-slate-500 text-sm">Select files for <strong>{EXAM_TYPES.find(e => e.id === selectedExamType)?.name}</strong></p>
                                            </div>
                                        )}
                                    </label>
                                </div>

                                <button
                                    onClick={handleUpload}
                                    disabled={uploading || files.length === 0}
                                    className="w-full py-3 bg-blue-600 hover:bg-blue-500 text-white rounded-xl font-medium transition-all flex items-center justify-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed shadow-lg shadow-blue-900/20"
                                >
                                    {uploading ? (
                                        <>
                                            <Loader2 className="animate-spin" size={18} />
                                            Processing...
                                        </>
                                    ) : (
                                        <>
                                            <Upload size={18} />
                                            Upload to {EXAM_TYPES.find(e => e.id === selectedExamType)?.name}
                                        </>
                                    )}
                                </button>

                                {status.message && (
                                    <div 
                                        className={`p-3 rounded-lg flex items-center gap-2 text-sm ${
                                            status.type === "success" 
                                            ? "bg-green-500/10 text-green-400 border border-green-500/20" 
                                            : "bg-red-500/10 text-red-400 border border-red-500/20"
                                        }`}
                                    >
                                        {status.type === "success" ? <CheckCircle size={16} /> : <AlertCircle size={16} />}
                                        {status.message}
                                    </div>
                                )}
                            </div>
                        </section>

                        {/* Document List with Tabs */}
                        <section className="bg-slate-900/50 border border-slate-800 rounded-2xl p-8 backdrop-blur-sm">
                            <div className="flex flex-col sm:flex-row items-center justify-between mb-6 gap-4">
                                <h3 className="text-lg font-medium text-slate-300">Active Documents</h3>
                                
                                {/* Tabs */}
                                <div className="flex p-1 bg-slate-950 rounded-lg border border-slate-800">
                                    {EXAM_TYPES.map((type) => {
                                        // Count documents for this type
                                        const count = documents.filter(d => {
                                            const dtype = d.topic || (d.subject.includes(":") ? d.subject.split(":")[0] : "IIT_JEE");
                                            return dtype === type.id || (type.id === "IIT_JEE" && !d.topic && !d.subject.includes(":"));
                                        }).length;
                                        
                                        return (
                                            <button
                                                key={type.id}
                                                onClick={() => setActiveTab(type.id)}
                                                className={`px-4 py-1.5 rounded-md text-sm font-medium transition-all flex items-center gap-2 ${
                                                    activeTab === type.id
                                                    ? "bg-slate-800 text-white shadow-sm"
                                                    : "text-slate-400 hover:text-slate-200"
                                                }`}
                                            >
                                                <span>{type.name}</span>
                                                <span className={`text-xs px-1.5 py-0.5 rounded-full ${
                                                    activeTab === type.id ? "bg-slate-950 text-slate-300" : "bg-slate-900 text-slate-500"
                                                }`}>
                                                    {count}
                                                </span>
                                            </button>
                                        );
                                    })}
                                </div>
                            </div>
                            
                            <div className="space-y-3 max-h-[400px] overflow-y-auto pr-2 custom-scrollbar">
                                {loadingDocs ? (
                                    <div className="text-center py-8 text-slate-500">Loading documents...</div>
                                ) : filteredDocuments.length === 0 ? (
                                    <div className="text-center py-12 border-2 border-dashed border-slate-800 rounded-xl">
                                        <p className="text-slate-500 mb-2">No documents for {EXAM_TYPES.find(e => e.id === activeTab)?.name} yet</p>
                                        <p className="text-xs text-slate-600">Select this exam type above and upload a PDF</p>
                                    </div>
                                ) : (
                                    filteredDocuments.map((doc) => {
                                        // Find exam type details for styling
                                        const docType = EXAM_TYPES.find(t => t.id === activeTab) || EXAM_TYPES[0];
                                        
                                        return (
                                            <div 
                                                key={doc.id} 
                                                className="flex items-center justify-between p-4 bg-slate-800/30 hover:bg-slate-800/50 rounded-lg border border-slate-800/50 transition-colors group"
                                            >
                                                <div className="flex items-center gap-4">
                                                    <div className={`w-10 h-10 rounded-lg ${docType.bg} flex items-center justify-center group-hover:bg-opacity-20 transition-colors`}>
                                                        <docType.icon className={docType.color} size={20} />
                                                    </div>
                                                    <div>
                                                        <span className="font-medium block text-slate-200 text-sm">{doc.filename}</span>
                                                        <span className="text-xs text-slate-500">
                                                            {new Date(doc.upload_date).toLocaleDateString()} • {doc.subject.split(":").pop()}
                                                        </span>
                                                    </div>
                                                </div>
                                                <div className="flex items-center gap-2">
                                                    <span className="text-[10px] uppercase font-bold text-green-400 bg-green-500/10 px-2 py-0.5 rounded border border-green-500/20">
                                                        Indexed
                                                    </span>
                                                </div>
                                            </div>
                                        );
                                    })
                                )}
                            </div>
                        </section>
                    </div>

                    {/* System Stats Sidebar */}
                    <div className="lg:col-span-1 space-y-8">
                        {/* Status Card */}
                        <div className="bg-slate-900/50 backdrop-blur-sm border border-slate-800 rounded-2xl p-6">
                            <h3 className="text-lg font-bold text-white mb-4 flex items-center gap-2">
                                <ActivityIcon className="text-green-400" />
                                System Health
                            </h3>
                            <div className="space-y-4">
                                <div className="p-4 bg-slate-950/50 rounded-xl border border-slate-800">
                                    <div className="flex items-center justify-between mb-2">
                                        <span className="text-slate-400 text-sm">RAG Engine</span>
                                        <span className="flex items-center gap-1.5 text-xs font-medium text-green-400 bg-green-500/10 px-2 py-1 rounded-full border border-green-500/20">
                                            <span className="w-1.5 h-1.5 rounded-full bg-green-400 animate-pulse"></span>
                                            Active
                                        </span>
                                    </div>
                                    <p className="text-xs text-slate-500">
                                        The question generation engine is currently using Retrieval Augmented Generation.
                                    </p>
                                </div>
                                
                                <div className="flex items-center justify-between p-3 rounded-lg bg-slate-800/30">
                                    <span className="text-slate-400 text-sm">Total Documents</span>
                                    <span className="font-mono text-white">{documents.length}</span>
                                </div>
                                
                                <button 
                                    onClick={syncVectorDB}
                                    disabled={syncing}
                                    className="w-full py-2 text-xs font-medium text-slate-400 hover:text-white bg-slate-800 hover:bg-slate-700 rounded-lg transition-colors flex items-center justify-center gap-2"
                                >
                                    {syncing ? <Loader2 size={14} className="animate-spin" /> : <RefreshCw size={14} />}
                                    Sync Vector Database
                                </button>
                            </div>
                        </div>

                        {/* Vector DB Stats */}
                        {vectorStats && (
                            <div className="bg-slate-900/50 backdrop-blur-sm border border-slate-800 rounded-2xl p-6">
                                <h3 className="text-lg font-bold text-white mb-4 flex items-center gap-2">
                                    <Database className="text-purple-400" />
                                    Vector DB Stats
                                </h3>
                                <div className="space-y-4">
                                    <div className="grid grid-cols-2 gap-4">
                                        <div className="p-3 bg-slate-950/50 rounded-xl border border-slate-800">
                                            <span className="block text-xs text-slate-500 mb-1">Total Vectors</span>
                                            <span className="text-xl font-bold text-white">{vectorStats.total_vector_count}</span>
                                        </div>
                                        <div className="p-3 bg-slate-950/50 rounded-xl border border-slate-800">
                                            <span className="block text-xs text-slate-500 mb-1">Dimension</span>
                                            <span className="text-xl font-bold text-white">{vectorStats.dimension}</span>
                                        </div>
                                    </div>
                                    
                                    <div className="p-3 bg-slate-950/50 rounded-xl border border-slate-800">
                                        <span className="block text-xs text-slate-500 mb-2">Namespaces</span>
                                        <div className="space-y-1">
                                            {Object.entries(vectorStats.namespaces).map(([ns, data]) => (
                                                <div key={ns} className="flex justify-between items-center text-xs">
                                                    <span className="text-slate-400">{ns || "default"}</span>
                                                    <span className="text-slate-200 font-mono">{data.vector_count} vectors</span>
                                                </div>
                                            ))}
                                        </div>
                                    </div>
                                </div>
                            </div>
                        )}
                    </div>
                </div>
            </main>
        </div>
    );
}

function ActivityIcon({ className }: { className?: string }) {
    return (
        <svg 
            xmlns="http://www.w3.org/2000/svg" 
            width="24" 
            height="24" 
            viewBox="0 0 24 24" 
            fill="none" 
            stroke="currentColor" 
            strokeWidth="2" 
            strokeLinecap="round" 
            strokeLinejoin="round" 
            className={className}
        >
            <path d="M22 12h-4l-3 9L9 3l-3 9H2" />
        </svg>
    );
}
