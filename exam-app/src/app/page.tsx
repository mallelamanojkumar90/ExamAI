"use client";

import { motion } from "framer-motion";
import Link from "next/link";
import { 
  Brain, TrendingUp, GraduationCap, CreditCard, 
  Users, Database, ArrowRight, Sparkles 
} from "lucide-react";

export default function LandingPage() {
  const features = [
    {
      icon: Brain,
      title: "AI-Powered Question Generation",
      description: "Generate contextual exam questions using RAG technology from your uploaded study materials.",
      color: "text-purple-400",
      bg: "bg-purple-500/10",
      border: "border-purple-500/20"
    },
    {
      icon: TrendingUp,
      title: "Performance Analytics",
      description: "Track your progress with detailed insights, subject-wise analysis, and AI-generated performance reports.",
      color: "text-blue-400",
      bg: "bg-blue-500/10",
      border: "border-blue-500/20"
    },
    {
      icon: GraduationCap,
      title: "Multiple Exam Types",
      description: "Prepare for IIT/JEE, NEET, and EAMCET with exam-specific patterns and difficulty levels.",
      color: "text-green-400",
      bg: "bg-green-500/10",
      border: "border-green-500/20"
    },
    {
      icon: CreditCard,
      title: "Flexible Subscription Plans",
      description: "Choose from monthly, quarterly, or annual plans with secure Razorpay payment integration.",
      color: "text-yellow-400",
      bg: "bg-yellow-500/10",
      border: "border-yellow-500/20"
    },
    {
      icon: Users,
      title: "Student Management",
      description: "Admins can monitor student progress, view exam history, and track performance metrics.",
      color: "text-pink-400",
      bg: "bg-pink-500/10",
      border: "border-pink-500/20"
    },
    {
      icon: Database,
      title: "Knowledge Base Management",
      description: "Upload PDFs and study materials to build a comprehensive RAG-powered knowledge base.",
      color: "text-cyan-400",
      bg: "bg-cyan-500/10",
      border: "border-cyan-500/20"
    }
  ];

  return (
    <div className="min-h-screen bg-slate-950 text-slate-200">
      {/* Navbar */}
      <nav className="border-b border-slate-800 bg-slate-950/80 backdrop-blur-sm sticky top-0 z-50">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <Link href="/" className="flex items-center gap-2">
              <div className="w-8 h-8 bg-gradient-to-br from-purple-500 to-pink-500 rounded-lg flex items-center justify-center">
                <Sparkles className="text-white" size={20} />
              </div>
              <span className="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-purple-400 to-pink-400">
                ExamAI
              </span>
            </Link>
            
            <div className="hidden md:flex items-center gap-8">
              <a href="#features" className="text-slate-400 hover:text-white transition-colors">
                Features
              </a>
              <a href="#pricing" className="text-slate-400 hover:text-white transition-colors">
                Pricing
              </a>
              <Link 
                href="/auth/login" 
                className="px-6 py-2 bg-gradient-to-r from-purple-500 to-pink-500 rounded-lg font-medium hover:opacity-90 transition-opacity"
              >
                Sign In / Register
              </Link>
            </div>

            {/* Mobile menu button */}
            <Link 
              href="/auth/login" 
              className="md:hidden px-4 py-2 bg-gradient-to-r from-purple-500 to-pink-500 rounded-lg text-sm font-medium"
            >
              Sign In
            </Link>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="relative overflow-hidden">
        {/* Background gradient effect */}
        <div className="absolute inset-0 bg-gradient-to-br from-purple-500/10 via-transparent to-pink-500/10 pointer-events-none" />
        
        <div className="container mx-auto px-4 py-24 md:py-32 relative">
          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            className="text-center max-w-4xl mx-auto"
          >
            <h1 className="text-5xl md:text-7xl font-bold mb-6 leading-tight">
              Elevate Your{" "}
              <span className="bg-clip-text text-transparent bg-gradient-to-r from-purple-400 via-pink-400 to-purple-400">
                Exam Preparation
              </span>
            </h1>
            
            <p className="text-xl md:text-2xl text-slate-400 mb-10 max-w-2xl mx-auto">
              Harness the power of AI to optimize your learning journey with personalized questions and intelligent analytics.
            </p>

            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link 
                href="/auth/signup"
                className="group px-8 py-4 bg-gradient-to-r from-purple-500 to-pink-500 rounded-xl font-semibold text-lg hover:opacity-90 transition-all flex items-center justify-center gap-2 shadow-lg shadow-purple-500/20"
              >
                Get Started
                <ArrowRight className="group-hover:translate-x-1 transition-transform" size={20} />
              </Link>
              
              <Link 
                href="/auth/login"
                className="px-8 py-4 bg-slate-800 hover:bg-slate-700 rounded-xl font-semibold text-lg transition-colors border border-slate-700"
              >
                Sign In
              </Link>
            </div>
          </motion.div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="py-24 bg-slate-900/50">
        <div className="container mx-auto px-4">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6 }}
            className="text-center mb-16"
          >
            <h2 className="text-4xl md:text-5xl font-bold mb-4">
              Powerful{" "}
              <span className="bg-clip-text text-transparent bg-gradient-to-r from-purple-400 to-pink-400">
                Features
              </span>
            </h2>
            <p className="text-xl text-slate-400 max-w-2xl mx-auto">
              Everything you need to ace your exams with AI-powered intelligence
            </p>
          </motion.div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 max-w-7xl mx-auto">
            {features.map((feature, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.5, delay: index * 0.1 }}
                whileHover={{ y: -5 }}
                className={`p-6 rounded-2xl border ${feature.border} ${feature.bg} backdrop-blur-sm hover:bg-opacity-80 transition-all group`}
              >
                <div className={`w-12 h-12 rounded-xl bg-slate-950/50 ${feature.color} flex items-center justify-center mb-4 group-hover:scale-110 transition-transform`}>
                  <feature.icon size={24} />
                </div>
                
                <h3 className="text-xl font-bold text-white mb-3">
                  {feature.title}
                </h3>
                
                <p className="text-slate-400 leading-relaxed">
                  {feature.description}
                </p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Pricing Section */}
      <section id="pricing" className="py-24">
        <div className="container mx-auto px-4">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6 }}
            className="text-center mb-16"
          >
            <h2 className="text-4xl md:text-5xl font-bold mb-4">
              Simple{" "}
              <span className="bg-clip-text text-transparent bg-gradient-to-r from-purple-400 to-pink-400">
                Pricing
              </span>
            </h2>
            <p className="text-xl text-slate-400 max-w-2xl mx-auto">
              Choose the plan that works best for you
            </p>
          </motion.div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-6xl mx-auto">
            {/* Monthly Plan */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.5 }}
              className="p-8 rounded-2xl border border-slate-700 bg-slate-900/50 backdrop-blur-sm hover:border-purple-500/50 transition-all"
            >
              <h3 className="text-2xl font-bold text-white mb-2">Monthly</h3>
              <div className="mb-6">
                <span className="text-4xl font-bold text-white">₹499</span>
                <span className="text-slate-400">/month</span>
              </div>
              <ul className="space-y-3 mb-8">
                <li className="flex items-start gap-2 text-slate-300">
                  <span className="text-green-400 mt-1">✓</span>
                  <span>Full access to all exams</span>
                </li>
                <li className="flex items-start gap-2 text-slate-300">
                  <span className="text-green-400 mt-1">✓</span>
                  <span>Unlimited practice tests</span>
                </li>
                <li className="flex items-start gap-2 text-slate-300">
                  <span className="text-green-400 mt-1">✓</span>
                  <span>Performance analytics</span>
                </li>
                <li className="flex items-start gap-2 text-slate-300">
                  <span className="text-green-400 mt-1">✓</span>
                  <span>Download reports (PDF)</span>
                </li>
                <li className="flex items-start gap-2 text-slate-300">
                  <span className="text-green-400 mt-1">✓</span>
                  <span>AI-powered questions</span>
                </li>
                <li className="flex items-start gap-2 text-slate-300">
                  <span className="text-green-400 mt-1">✓</span>
                  <span>24/7 support</span>
                </li>
              </ul>
              <Link
                href="/auth/signup"
                className="block w-full py-3 bg-slate-800 hover:bg-slate-700 rounded-xl font-semibold text-center transition-colors border border-slate-700"
              >
                Get Started
              </Link>
            </motion.div>

            {/* Quarterly Plan */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.5, delay: 0.1 }}
              className="p-8 rounded-2xl border border-slate-700 bg-slate-900/50 backdrop-blur-sm hover:border-purple-500/50 transition-all"
            >
              <div className="flex items-center justify-between mb-2">
                <h3 className="text-2xl font-bold text-white">Quarterly</h3>
                <span className="px-3 py-1 bg-green-500/10 text-green-400 rounded-full text-xs font-semibold border border-green-500/20">
                  SAVE 10%
                </span>
              </div>
              <div className="mb-2">
                <span className="text-4xl font-bold text-white">₹1,347</span>
                <span className="text-slate-400">/3 months</span>
              </div>
              <p className="text-sm text-slate-500 mb-6 line-through">₹1,497</p>
              <ul className="space-y-3 mb-8">
                <li className="flex items-start gap-2 text-slate-300">
                  <span className="text-green-400 mt-1">✓</span>
                  <span>All Monthly features</span>
                </li>
                <li className="flex items-start gap-2 text-slate-300">
                  <span className="text-green-400 mt-1">✓</span>
                  <span>₹449/month effective</span>
                </li>
                <li className="flex items-start gap-2 text-slate-300">
                  <span className="text-green-400 mt-1">✓</span>
                  <span>Priority support</span>
                </li>
                <li className="flex items-start gap-2 text-slate-300">
                  <span className="text-green-400 mt-1">✓</span>
                  <span>Advanced analytics</span>
                </li>
                <li className="flex items-start gap-2 text-slate-300">
                  <span className="text-green-400 mt-1">✓</span>
                  <span>Study material downloads</span>
                </li>
              </ul>
              <Link
                href="/auth/signup"
                className="block w-full py-3 bg-slate-800 hover:bg-slate-700 rounded-xl font-semibold text-center transition-colors border border-slate-700"
              >
                Get Started
              </Link>
            </motion.div>

            {/* Annual Plan - Recommended */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.5, delay: 0.2 }}
              className="p-8 rounded-2xl border-2 border-purple-500/50 bg-gradient-to-br from-purple-500/10 to-pink-500/10 backdrop-blur-sm relative overflow-hidden"
            >
              <div className="absolute top-4 right-4 px-3 py-1 bg-gradient-to-r from-purple-500 to-pink-500 rounded-full text-xs font-bold">
                RECOMMENDED
              </div>
              <h3 className="text-2xl font-bold text-white mb-2">Annual</h3>
              <div className="flex items-center gap-2 mb-2">
                <span className="px-3 py-1 bg-pink-500/10 text-pink-400 rounded-full text-xs font-semibold border border-pink-500/20">
                  SAVE 20%
                </span>
              </div>
              <div className="mb-2">
                <span className="text-4xl font-bold text-white">₹4,788</span>
                <span className="text-slate-400">/year</span>
              </div>
              <p className="text-sm text-slate-500 mb-6 line-through">₹5,988</p>
              <ul className="space-y-3 mb-8">
                <li className="flex items-start gap-2 text-slate-300">
                  <span className="text-green-400 mt-1">✓</span>
                  <span>All Quarterly features</span>
                </li>
                <li className="flex items-start gap-2 text-slate-300">
                  <span className="text-green-400 mt-1">✓</span>
                  <span>₹399/month effective</span>
                </li>
                <li className="flex items-start gap-2 text-slate-300">
                  <span className="text-green-400 mt-1">✓</span>
                  <span>Dedicated support</span>
                </li>
                <li className="flex items-start gap-2 text-slate-300">
                  <span className="text-green-400 mt-1">✓</span>
                  <span>Early access to features</span>
                </li>
                <li className="flex items-start gap-2 text-slate-300">
                  <span className="text-green-400 mt-1">✓</span>
                  <span>Interview preparation</span>
                </li>
                <li className="flex items-start gap-2 text-slate-300">
                  <span className="text-green-400 mt-1">✓</span>
                  <span>Personalized learning path</span>
                </li>
              </ul>
              <Link
                href="/auth/signup"
                className="block w-full py-3 bg-gradient-to-r from-purple-500 to-pink-500 hover:opacity-90 rounded-xl font-semibold text-center transition-opacity"
              >
                Get Started
              </Link>
            </motion.div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-24">
        <div className="container mx-auto px-4">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6 }}
            className="max-w-4xl mx-auto text-center bg-gradient-to-br from-purple-500/10 to-pink-500/10 rounded-3xl p-12 border border-purple-500/20"
          >
            <h2 className="text-4xl md:text-5xl font-bold mb-6">
              Ready to Transform Your{" "}
              <span className="bg-clip-text text-transparent bg-gradient-to-r from-purple-400 to-pink-400">
                Exam Preparation?
              </span>
            </h2>
            
            <p className="text-xl text-slate-400 mb-8 max-w-2xl mx-auto">
              Join thousands of students already using AI to achieve their academic goals.
            </p>

            <Link 
              href="/auth/signup"
              className="inline-flex items-center gap-2 px-8 py-4 bg-gradient-to-r from-purple-500 to-pink-500 rounded-xl font-semibold text-lg hover:opacity-90 transition-all shadow-lg shadow-purple-500/20"
            >
              Start Free Trial
              <ArrowRight size={20} />
            </Link>
          </motion.div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-slate-800 py-8">
        <div className="container mx-auto px-4">
          <div className="text-center text-slate-500">
            <p>&copy; 2025 ExamAI. All rights reserved.</p>
          </div>
        </div>
      </footer>

    </div>
  );
}
