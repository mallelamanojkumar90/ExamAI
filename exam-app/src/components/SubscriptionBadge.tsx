"use client";

import { useEffect, useState } from "react";
import { Crown, Clock } from "lucide-react";

interface SubscriptionBadgeProps {
  userId: number;
  showDetails?: boolean;
}

export default function SubscriptionBadge({
  userId,
  showDetails = false,
}: SubscriptionBadgeProps) {
  const [hasSubscription, setHasSubscription] = useState(false);
  const [daysRemaining, setDaysRemaining] = useState(0);
  const [planType, setPlanType] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchSubscriptionStatus();
  }, [userId]);

  const fetchSubscriptionStatus = async () => {
    try {
      const response = await fetch(
        `http://localhost:8000/api/subscription/status/${userId}`
      );
      const data = await response.json();
      if (data.success && data.has_active_subscription) {
        setHasSubscription(true);
        setDaysRemaining(data.subscription.days_remaining);
        setPlanType(data.subscription.plan_type);
      }
    } catch (error) {
      console.error("Error fetching subscription:", error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return null;
  }

  if (!hasSubscription) {
    return (
      <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-gray-700/50 border border-gray-600">
        <div className="w-2 h-2 bg-gray-400 rounded-full"></div>
        <span className="text-gray-300 text-sm font-medium">Free</span>
      </div>
    );
  }

  const getColorClass = () => {
    if (daysRemaining <= 7) {
      return "from-red-500 to-orange-500";
    } else if (daysRemaining <= 30) {
      return "from-yellow-500 to-orange-500";
    } else {
      return "from-green-500 to-emerald-500";
    }
  };

  return (
    <div
      className={`inline-flex items-center gap-2 px-3 py-1 rounded-full bg-gradient-to-r ${getColorClass()} shadow-lg`}
    >
      <Crown className="w-4 h-4 text-white" />
      <span className="text-white text-sm font-semibold capitalize">
        {planType}
      </span>
      {showDetails && (
        <>
          <div className="w-px h-4 bg-white/30"></div>
          <div className="flex items-center gap-1">
            <Clock className="w-3 h-3 text-white" />
            <span className="text-white text-xs">{daysRemaining}d left</span>
          </div>
        </>
      )}
    </div>
  );
}
