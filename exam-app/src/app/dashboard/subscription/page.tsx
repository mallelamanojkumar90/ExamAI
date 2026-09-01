"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import {
  Calendar,
  CreditCard,
  Download,
  AlertCircle,
  CheckCircle,
  XCircle,
} from "lucide-react";

interface Subscription {
  subscription_id: number;
  plan_type: string;
  start_date: string;
  end_date: string;
  days_remaining: number;
  amount: number;
  auto_renew: boolean;
}

interface Payment {
  payment_id: number;
  amount: number;
  payment_method: string;
  transaction_id: string;
  status: string;
  payment_date: string;
  invoice_available: boolean;
}

export default function SubscriptionDashboardPage() {
  const router = useRouter();
  const [subscription, setSubscription] = useState<Subscription | null>(null);
  const [payments, setPayments] = useState<Payment[]>([]);
  const [loading, setLoading] = useState(true);
  const [userId] = useState(1); // In real app, get from auth

  useEffect(() => {
    fetchSubscriptionStatus();
    fetchPaymentHistory();
  }, []);

  const fetchSubscriptionStatus = async () => {
    try {
      const response = await fetch(
        `http://localhost:8000/api/subscription/status/${userId}`
      );
      const data = await response.json();
      if (data.success && data.has_active_subscription) {
        setSubscription(data.subscription);
      }
    } catch (error) {
      console.error("Error fetching subscription:", error);
    } finally {
      setLoading(false);
    }
  };

  const fetchPaymentHistory = async () => {
    try {
      const response = await fetch(
        `http://localhost:8000/api/payment/history/${userId}`
      );
      const data = await response.json();
      if (data.success) {
        setPayments(data.payments);
      }
    } catch (error) {
      console.error("Error fetching payments:", error);
    }
  };

  const handleDownloadInvoice = async (paymentId: number) => {
    try {
      const response = await fetch(
        `http://localhost:8000/api/payment/invoice/${paymentId}`
      );
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `invoice_${paymentId}.pdf`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
    } catch (error) {
      console.error("Error downloading invoice:", error);
      alert("Failed to download invoice");
    }
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString("en-US", {
      year: "numeric",
      month: "long",
      day: "numeric",
    });
  };

  const getStatusColor = (status: string) => {
    switch (status.toLowerCase()) {
      case "success":
        return "text-green-400";
      case "failed":
        return "text-red-400";
      case "pending":
        return "text-yellow-400";
      default:
        return "text-gray-400";
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status.toLowerCase()) {
      case "success":
        return <CheckCircle className="w-5 h-5 text-green-400" />;
      case "failed":
        return <XCircle className="w-5 h-5 text-red-400" />;
      case "pending":
        return <AlertCircle className="w-5 h-5 text-yellow-400" />;
      default:
        return null;
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 flex items-center justify-center">
        <div className="text-white text-xl">Loading...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-white mb-2">
            Subscription Management
          </h1>
          <p className="text-gray-300">
            Manage your subscription and view payment history
          </p>
        </div>

        {/* Current Subscription */}
        {subscription ? (
          <div className="bg-white/5 backdrop-blur-lg rounded-2xl p-6 border border-gray-700 mb-8">
            <h2 className="text-2xl font-bold text-white mb-6">
              Current Subscription
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div>
                <p className="text-gray-400 text-sm mb-1">Plan</p>
                <p className="text-white text-xl font-semibold capitalize">
                  {subscription.plan_type} Plan
                </p>
              </div>
              <div>
                <p className="text-gray-400 text-sm mb-1">Status</p>
                <div className="flex items-center gap-2">
                  <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
                  <p className="text-green-400 text-xl font-semibold">Active</p>
                </div>
              </div>
              <div>
                <p className="text-gray-400 text-sm mb-1">Days Remaining</p>
                <p className="text-white text-xl font-semibold">
                  {subscription.days_remaining} days
                </p>
              </div>
            </div>

            <div className="mt-6 pt-6 border-t border-gray-700">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="flex items-center gap-3">
                  <Calendar className="w-5 h-5 text-blue-400" />
                  <div>
                    <p className="text-gray-400 text-sm">Start Date</p>
                    <p className="text-white">
                      {formatDate(subscription.start_date)}
                    </p>
                  </div>
                </div>
                <div className="flex items-center gap-3">
                  <Calendar className="w-5 h-5 text-red-400" />
                  <div>
                    <p className="text-gray-400 text-sm">End Date</p>
                    <p className="text-white">
                      {formatDate(subscription.end_date)}
                    </p>
                  </div>
                </div>
              </div>
            </div>

            <div className="mt-6 flex gap-4">
              <button
                onClick={() => router.push("/subscription")}
                className="px-6 py-2 rounded-lg font-semibold text-white bg-gradient-to-r from-blue-500 to-blue-600 hover:from-blue-600 hover:to-blue-700 transition-all duration-300"
              >
                Upgrade Plan
              </button>
            </div>
          </div>
        ) : (
          <div className="bg-white/5 backdrop-blur-lg rounded-2xl p-8 border border-gray-700 mb-8 text-center">
            <AlertCircle className="w-16 h-16 text-yellow-400 mx-auto mb-4" />
            <h2 className="text-2xl font-bold text-white mb-2">
              No Active Subscription
            </h2>
            <p className="text-gray-300 mb-6">
              Subscribe now to get unlimited access to all features
            </p>
            <button
              onClick={() => router.push("/subscription")}
              className="px-8 py-3 rounded-lg font-semibold text-white bg-gradient-to-r from-blue-500 to-blue-600 hover:from-blue-600 hover:to-blue-700 transition-all duration-300"
            >
              View Plans
            </button>
          </div>
        )}

        {/* Payment History */}
        <div className="bg-white/5 backdrop-blur-lg rounded-2xl p-6 border border-gray-700">
          <h2 className="text-2xl font-bold text-white mb-6">
            Payment History
          </h2>

          {payments.length > 0 ? (
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="border-b border-gray-700">
                    <th className="text-left text-gray-400 font-semibold py-3 px-4">
                      Date
                    </th>
                    <th className="text-left text-gray-400 font-semibold py-3 px-4">
                      Amount
                    </th>
                    <th className="text-left text-gray-400 font-semibold py-3 px-4">
                      Method
                    </th>
                    <th className="text-left text-gray-400 font-semibold py-3 px-4">
                      Status
                    </th>
                    <th className="text-left text-gray-400 font-semibold py-3 px-4">
                      Invoice
                    </th>
                  </tr>
                </thead>
                <tbody>
                  {payments.map((payment) => (
                    <tr
                      key={payment.payment_id}
                      className="border-b border-gray-800 hover:bg-white/5 transition-colors"
                    >
                      <td className="py-4 px-4 text-gray-200">
                        {formatDate(payment.payment_date)}
                      </td>
                      <td className="py-4 px-4 text-white font-semibold">
                        ₹{payment.amount}
                      </td>
                      <td className="py-4 px-4 text-gray-200 capitalize">
                        {payment.payment_method}
                      </td>
                      <td className="py-4 px-4">
                        <div className="flex items-center gap-2">
                          {getStatusIcon(payment.status)}
                          <span
                            className={`capitalize ${getStatusColor(
                              payment.status
                            )}`}
                          >
                            {payment.status}
                          </span>
                        </div>
                      </td>
                      <td className="py-4 px-4">
                        {payment.invoice_available ? (
                          <button
                            onClick={() =>
                              handleDownloadInvoice(payment.payment_id)
                            }
                            className="flex items-center gap-2 text-blue-400 hover:text-blue-300 transition-colors"
                          >
                            <Download className="w-4 h-4" />
                            Download
                          </button>
                        ) : (
                          <span className="text-gray-500">N/A</span>
                        )}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ) : (
            <div className="text-center py-8">
              <CreditCard className="w-16 h-16 text-gray-600 mx-auto mb-4" />
              <p className="text-gray-400">No payment history yet</p>
            </div>
          )}
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
