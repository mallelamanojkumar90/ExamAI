"use client";

import { useRouter } from "next/navigation";
import { XCircle, RefreshCw, HelpCircle } from "lucide-react";

export default function PaymentFailurePage() {
  const router = useRouter();

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 flex items-center justify-center px-4">
      <div className="max-w-md w-full">
        <div className="bg-white/5 backdrop-blur-lg rounded-2xl p-8 border border-red-500/30 shadow-2xl shadow-red-500/20 text-center">
          {/* Failure Icon */}
          <div className="mb-6 flex justify-center">
            <div className="bg-red-500/20 rounded-full p-6">
              <XCircle className="w-16 h-16 text-red-400" />
            </div>
          </div>

          {/* Failure Message */}
          <h1 className="text-3xl font-bold text-white mb-4">
            Payment Failed
          </h1>
          <p className="text-gray-300 mb-8">
            We couldn't process your payment. Don't worry, no charges were made
            to your account.
          </p>

          {/* Common Reasons */}
          <div className="bg-white/5 rounded-lg p-6 mb-8 text-left">
            <h2 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
              <HelpCircle className="w-5 h-5" />
              Common Reasons
            </h2>
            <ul className="space-y-2 text-gray-200 text-sm">
              <li>• Insufficient funds in your account</li>
              <li>• Incorrect card details or CVV</li>
              <li>• Card expired or blocked</li>
              <li>• Network connectivity issues</li>
              <li>• Payment cancelled by user</li>
            </ul>
          </div>

          {/* Action Buttons */}
          <div className="space-y-3">
            <button
              onClick={() => router.push("/subscription")}
              className="w-full py-3 rounded-lg font-semibold text-white bg-gradient-to-r from-blue-500 to-blue-600 hover:from-blue-600 hover:to-blue-700 transition-all duration-300 shadow-lg flex items-center justify-center gap-2"
            >
              <RefreshCw className="w-5 h-5" />
              Try Again
            </button>
            <button
              onClick={() => router.push("/dashboard")}
              className="w-full py-3 rounded-lg font-semibold text-gray-300 bg-white/5 hover:bg-white/10 transition-all duration-300 border border-gray-600"
            >
              Back to Dashboard
            </button>
          </div>

          {/* Support */}
          <div className="mt-8 pt-6 border-t border-gray-700">
            <p className="text-gray-400 text-sm mb-2">Need help?</p>
            <a
              href="mailto:support@examplatform.com"
              className="text-blue-400 hover:text-blue-300 text-sm"
            >
              Contact Support
            </a>
          </div>
        </div>
      </div>
    </div>
  );
}
