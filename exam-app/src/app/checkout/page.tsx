"use client";

import { useState, useEffect } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { Lock, CreditCard, CheckCircle } from "lucide-react";

declare global {
  interface Window {
    Razorpay: any;
  }
}

interface Plan {
  id: string;
  name: string;
  price: number;
  duration_days: number;
  discount: number;
  original_price: number;
  features: string[];
}

export default function CheckoutPage() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const planType = searchParams.get("plan");

  const [plan, setPlan] = useState<Plan | null>(null);
  const [loading, setLoading] = useState(true);
  const [processing, setProcessing] = useState(false);
  const [userId, setUserId] = useState<number | null>(null);

  useEffect(() => {
    // Load Razorpay script
    const script = document.createElement("script");
    script.src = "https://checkout.razorpay.com/v1/checkout.js";
    script.async = true;
    document.body.appendChild(script);

    // Get user info
    const user = localStorage.getItem("user");
    if (!user) {
      router.push("/");
      return;
    }

    // Fetch user ID (in real app, this would come from auth)
    // For now, we'll use a placeholder
    setUserId(1);

    if (planType) {
      fetchPlanDetails(planType);
    }

    return () => {
      document.body.removeChild(script);
    };
  }, [planType]);

  const fetchPlanDetails = async (planId: string) => {
    try {
      const response = await fetch(
        `http://localhost:8000/api/subscription/plan/${planId}`
      );
      const data = await response.json();
      if (data.success) {
        setPlan(data.plan);
      }
    } catch (error) {
      console.error("Error fetching plan:", error);
    } finally {
      setLoading(false);
    }
  };

  const handlePayment = async () => {
    if (!plan || !userId) return;

    setProcessing(true);

    try {
      // Create order
      const orderResponse = await fetch(
        "http://localhost:8000/api/payment/create-order",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            user_id: userId,
            plan_type: plan.id,
          }),
        }
      );

      const orderData = await orderResponse.json();

      if (!orderData.success) {
        throw new Error("Failed to create order");
      }

      // Razorpay options
      const options = {
        key: orderData.key_id,
        amount: orderData.amount * 100, // Convert to paise
        currency: orderData.currency,
        name: "Exam Platform",
        description: `${plan.name} Subscription`,
        order_id: orderData.order_id,
        handler: async function (response: any) {
          // Verify payment
          try {
            const verifyResponse = await fetch(
              "http://localhost:8000/api/payment/verify",
              {
                method: "POST",
                headers: {
                  "Content-Type": "application/json",
                },
                body: JSON.stringify({
                  razorpay_order_id: response.razorpay_order_id,
                  razorpay_payment_id: response.razorpay_payment_id,
                  razorpay_signature: response.razorpay_signature,
                  user_id: userId,
                  plan_type: plan.id,
                }),
              }
            );

            const verifyData = await verifyResponse.json();

            if (verifyData.success) {
              router.push("/payment/success");
            } else {
              router.push("/payment/failure");
            }
          } catch (error) {
            console.error("Payment verification error:", error);
            router.push("/payment/failure");
          }
        },
        prefill: {
          name: localStorage.getItem("user") || "",
          email: localStorage.getItem("user") || "",
        },
        theme: {
          color: "#3B82F6",
        },
        modal: {
          ondismiss: function () {
            setProcessing(false);
          },
        },
      };

      const razorpay = new window.Razorpay(options);
      razorpay.open();
    } catch (error) {
      console.error("Payment error:", error);
      alert("Failed to initiate payment. Please try again.");
      setProcessing(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 flex items-center justify-center">
        <div className="text-white text-xl">Loading...</div>
      </div>
    );
  }

  if (!plan) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 flex items-center justify-center">
        <div className="text-white text-xl">Plan not found</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-white mb-2">Checkout</h1>
          <p className="text-gray-300">Complete your subscription</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          {/* Order Summary */}
          <div className="bg-white/5 backdrop-blur-lg rounded-2xl p-6 border border-gray-700">
            <h2 className="text-2xl font-bold text-white mb-6">
              Order Summary
            </h2>

            <div className="space-y-4">
              <div>
                <h3 className="text-lg font-semibold text-white">
                  {plan.name}
                </h3>
                <p className="text-gray-300 text-sm">
                  {plan.duration_days} days access
                </p>
              </div>

              <div className="border-t border-gray-700 pt-4">
                <div className="flex justify-between text-gray-300 mb-2">
                  <span>Subtotal</span>
                  <span>₹{plan.original_price}</span>
                </div>
                {plan.discount > 0 && (
                  <div className="flex justify-between text-green-400 mb-2">
                    <span>Discount ({plan.discount}%)</span>
                    <span>-₹{plan.original_price - plan.price}</span>
                  </div>
                )}
                <div className="flex justify-between text-white text-xl font-bold mt-4 pt-4 border-t border-gray-700">
                  <span>Total</span>
                  <span>₹{plan.price}</span>
                </div>
              </div>

              <div className="bg-blue-500/10 border border-blue-500/30 rounded-lg p-4 mt-6">
                <h4 className="text-white font-semibold mb-2">
                  What's included:
                </h4>
                <ul className="space-y-2">
                  {plan.features.slice(0, 4).map((feature, index) => (
                    <li key={index} className="flex items-start gap-2">
                      <CheckCircle className="w-4 h-4 text-green-400 flex-shrink-0 mt-0.5" />
                      <span className="text-gray-200 text-sm">{feature}</span>
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          </div>

          {/* Payment Section */}
          <div className="bg-white/5 backdrop-blur-lg rounded-2xl p-6 border border-gray-700">
            <h2 className="text-2xl font-bold text-white mb-6">Payment</h2>

            <div className="space-y-6">
              <div className="bg-white/5 rounded-lg p-4 border border-gray-600">
                <div className="flex items-center gap-3 mb-3">
                  <CreditCard className="w-6 h-6 text-blue-400" />
                  <span className="text-white font-semibold">
                    Secure Payment
                  </span>
                </div>
                <p className="text-gray-300 text-sm">
                  Your payment is processed securely through Razorpay. We
                  support UPI, Cards, Net Banking, and Wallets.
                </p>
              </div>

              <button
                onClick={handlePayment}
                disabled={processing}
                className="w-full py-4 rounded-lg font-semibold text-white bg-gradient-to-r from-blue-500 to-blue-600 hover:from-blue-600 hover:to-blue-700 transition-all duration-300 shadow-lg disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
              >
                {processing ? (
                  <>
                    <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
                    Processing...
                  </>
                ) : (
                  <>
                    <Lock className="w-5 h-5" />
                    Pay ₹{plan.price}
                  </>
                )}
              </button>

              <div className="flex items-center justify-center gap-2 text-gray-400 text-sm">
                <Lock className="w-4 h-4" />
                <span>Secured by Razorpay</span>
              </div>

              <div className="text-center text-gray-400 text-xs">
                By completing this purchase, you agree to our Terms of Service
                and Privacy Policy
              </div>
            </div>
          </div>
        </div>

        {/* Back Button */}
        <div className="text-center mt-8">
          <button
            onClick={() => router.push("/subscription")}
            className="text-gray-300 hover:text-white transition-colors"
          >
            ← Back to Plans
          </button>
        </div>
      </div>
    </div>
  );
}
