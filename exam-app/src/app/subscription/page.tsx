"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { Check, Sparkles } from "lucide-react";

interface Plan {
  id: string;
  name: string;
  price: number;
  duration_days: number;
  discount: number;
  original_price: number;
  features: string[];
  recommended?: boolean;
}

export default function SubscriptionPage() {
  const router = useRouter();
  const [plans, setPlans] = useState<Plan[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedPlan, setSelectedPlan] = useState<string | null>(null);

  useEffect(() => {
    fetchPlans();
  }, []);

  const fetchPlans = async () => {
    try {
      const response = await fetch("http://localhost:8000/api/subscription/plans");
      const data = await response.json();
      if (data.success) {
        setPlans(data.plans);
      }
    } catch (error) {
      console.error("Error fetching plans:", error);
    } finally {
      setLoading(false);
    }
  };

  const handleSelectPlan = (planId: string) => {
    const user = localStorage.getItem("user");
    if (!user) {
      router.push("/");
      return;
    }
    router.push(`/checkout?plan=${planId}`);
  };

  const getPlanColor = (planId: string) => {
    switch (planId) {
      case "monthly":
        return "from-blue-500 to-blue-600";
      case "quarterly":
        return "from-purple-500 to-purple-600";
      case "annual":
        return "from-green-500 to-green-600";
      default:
        return "from-gray-500 to-gray-600";
    }
  };

  const getPlanBorderColor = (planId: string) => {
    switch (planId) {
      case "monthly":
        return "border-blue-500";
      case "quarterly":
        return "border-purple-500";
      case "annual":
        return "border-green-500";
      default:
        return "border-gray-500";
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 flex items-center justify-center">
        <div className="text-white text-xl">Loading plans...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="text-center mb-16">
          <h1 className="text-5xl font-bold text-white mb-4">
            Choose Your Plan
          </h1>
          <p className="text-xl text-gray-300">
            Unlock unlimited access to exam preparation resources
          </p>
        </div>

        {/* Pricing Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-12">
          {plans.map((plan) => (
            <div
              key={plan.id}
              className={`relative bg-white/5 backdrop-blur-lg rounded-2xl p-8 border-2 ${
                plan.recommended
                  ? "border-green-500 shadow-2xl shadow-green-500/20 scale-105"
                  : getPlanBorderColor(plan.id)
              } hover:scale-105 transition-all duration-300`}
            >
              {/* Recommended Badge */}
              {plan.recommended && (
                <div className="absolute -top-4 left-1/2 transform -translate-x-1/2">
                  <div className="bg-gradient-to-r from-green-500 to-green-600 text-white px-4 py-1 rounded-full text-sm font-semibold flex items-center gap-1">
                    <Sparkles className="w-4 h-4" />
                    Most Popular
                  </div>
                </div>
              )}

              {/* Plan Header */}
              <div className="text-center mb-6">
                <h3 className="text-2xl font-bold text-white mb-2">
                  {plan.name}
                </h3>
                <div className="flex items-center justify-center gap-2">
                  {plan.discount > 0 && (
                    <span className="text-gray-400 line-through text-lg">
                      ₹{plan.original_price}
                    </span>
                  )}
                  <span className="text-4xl font-bold text-white">
                    ₹{plan.price}
                  </span>
                </div>
                <p className="text-gray-300 mt-2">
                  {plan.duration_days} days
                  {plan.discount > 0 && (
                    <span className="ml-2 text-green-400 font-semibold">
                      Save {plan.discount}%
                    </span>
                  )}
                </p>
              </div>

              {/* Features List */}
              <ul className="space-y-3 mb-8">
                {plan.features.map((feature, index) => (
                  <li key={index} className="flex items-start gap-2">
                    <Check className="w-5 h-5 text-green-400 flex-shrink-0 mt-0.5" />
                    <span className="text-gray-200 text-sm">{feature}</span>
                  </li>
                ))}
              </ul>

              {/* CTA Button */}
              <button
                onClick={() => handleSelectPlan(plan.id)}
                className={`w-full py-3 rounded-lg font-semibold text-white bg-gradient-to-r ${getPlanColor(
                  plan.id
                )} hover:opacity-90 transition-all duration-300 shadow-lg`}
              >
                Choose {plan.name}
              </button>
            </div>
          ))}
        </div>

        {/* Features Comparison */}
        <div className="bg-white/5 backdrop-blur-lg rounded-2xl p-8 border border-gray-700">
          <h2 className="text-2xl font-bold text-white mb-6 text-center">
            All Plans Include
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="text-center">
              <div className="text-4xl mb-2">📚</div>
              <h3 className="text-lg font-semibold text-white mb-2">
                Unlimited Exams
              </h3>
              <p className="text-gray-300 text-sm">
                Practice as many times as you want
              </p>
            </div>
            <div className="text-center">
              <div className="text-4xl mb-2">🤖</div>
              <h3 className="text-lg font-semibold text-white mb-2">
                AI-Powered Questions
              </h3>
              <p className="text-gray-300 text-sm">
                Get unique questions every time
              </p>
            </div>
            <div className="text-center">
              <div className="text-4xl mb-2">📊</div>
              <h3 className="text-lg font-semibold text-white mb-2">
                Performance Analytics
              </h3>
              <p className="text-gray-300 text-sm">
                Track your progress over time
              </p>
            </div>
          </div>
        </div>

        {/* Back Button */}
        <div className="text-center mt-8">
          <button
            onClick={() => router.push("/dashboard")}
            className="text-gray-300 hover:text-white transition-colors"
          >
            ← Back to Dashboard
          </button>
        </div>
      </div>
    </div>
  );
}
