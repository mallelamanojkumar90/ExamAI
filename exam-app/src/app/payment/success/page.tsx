"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { CheckCircle, ArrowRight } from "lucide-react";

export default function PaymentSuccessPage() {
  const router = useRouter();

  useEffect(() => {
    // Confetti animation (optional)
    const duration = 3 * 1000;
    const animationEnd = Date.now() + duration;

    const randomInRange = (min: number, max: number) => {
      return Math.random() * (max - min) + min;
    };

    const interval = setInterval(() => {
      const timeLeft = animationEnd - Date.now();

      if (timeLeft <= 0) {
        return clearInterval(interval);
      }

      // Simple confetti effect using emoji
      const particle = document.createElement("div");
      particle.innerHTML = "🎉";
      particle.style.position = "fixed";
      particle.style.left = Math.random() * 100 + "%";
      particle.style.top = "-20px";
      particle.style.fontSize = "30px";
      particle.style.zIndex = "9999";
      particle.style.pointerEvents = "none";
      document.body.appendChild(particle);

      const animation = particle.animate(
        [
          { transform: "translateY(0) rotate(0deg)", opacity: 1 },
          {
            transform: `translateY(${window.innerHeight}px) rotate(${
              randomInRange(-180, 180)
            }deg)`,
            opacity: 0,
          },
        ],
        {
          duration: randomInRange(2000, 4000),
          easing: "cubic-bezier(0, .9, .57, 1)",
        }
      );

      animation.onfinish = () => {
        particle.remove();
      };
    }, 200);

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 flex items-center justify-center px-4">
      <div className="max-w-md w-full">
        <div className="bg-white/5 backdrop-blur-lg rounded-2xl p-8 border border-green-500/30 shadow-2xl shadow-green-500/20 text-center">
          {/* Success Icon */}
          <div className="mb-6 flex justify-center">
            <div className="bg-green-500/20 rounded-full p-6">
              <CheckCircle className="w-16 h-16 text-green-400" />
            </div>
          </div>

          {/* Success Message */}
          <h1 className="text-3xl font-bold text-white mb-4">
            Payment Successful!
          </h1>
          <p className="text-gray-300 mb-8">
            Your subscription has been activated successfully. You now have full
            access to all premium features!
          </p>

          {/* What's Next */}
          <div className="bg-white/5 rounded-lg p-6 mb-8 text-left">
            <h2 className="text-lg font-semibold text-white mb-4">
              What's Next?
            </h2>
            <ul className="space-y-3">
              <li className="flex items-start gap-3">
                <span className="text-green-400 font-bold">1.</span>
                <span className="text-gray-200 text-sm">
                  Check your email for the invoice and subscription details
                </span>
              </li>
              <li className="flex items-start gap-3">
                <span className="text-green-400 font-bold">2.</span>
                <span className="text-gray-200 text-sm">
                  Start practicing with unlimited exam access
                </span>
              </li>
              <li className="flex items-start gap-3">
                <span className="text-green-400 font-bold">3.</span>
                <span className="text-gray-200 text-sm">
                  Track your progress in the dashboard
                </span>
              </li>
            </ul>
          </div>

          {/* Action Buttons */}
          <div className="space-y-3">
            <button
              onClick={() => router.push("/dashboard")}
              className="w-full py-3 rounded-lg font-semibold text-white bg-gradient-to-r from-green-500 to-green-600 hover:from-green-600 hover:to-green-700 transition-all duration-300 shadow-lg flex items-center justify-center gap-2"
            >
              Go to Dashboard
              <ArrowRight className="w-5 h-5" />
            </button>
            <button
              onClick={() => router.push("/dashboard/subscription")}
              className="w-full py-3 rounded-lg font-semibold text-gray-300 bg-white/5 hover:bg-white/10 transition-all duration-300 border border-gray-600"
            >
              View Subscription Details
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
