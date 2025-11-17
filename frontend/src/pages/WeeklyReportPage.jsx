// frontend/src/pages/WeeklyReportPage.jsx — AdVision Dark Responsive Upgrade
import React, { useState, useEffect } from "react";
import apiClient from "../api/client";
import toast from "react-hot-toast";
import {
  BarChart3,
  Zap,
  Lightbulb,
  TrendingUp,
  Download,
  Clock,
  Layers,
  Target,
  CheckCircle,
} from "lucide-react";

export default function WeeklyReportPage() {
  const [report, setReport] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    fetchReport();
  }, []);

  const fetchReport = async () => {
    setIsLoading(true);
    try {
      const response = await apiClient.get("/reports/weekly/");
      setReport(response.data);
    } catch (error) {
      toast.error("Failed to load weekly report.");
    } finally {
      setIsLoading(false);
    }
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-[#0f0c12]">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-[#a88fd8]" />
      </div>
    );
  }

  if (!report) {
    return (
      <div className="text-center text-gray-400 py-20 bg-[#0f0c12]">
        No report available
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-[#0f0c12] via-[#16111d] to-[#0d0b11] text-white p-4 sm:p-6 md:p-8">

      {/* Header */}
      <div className="mb-10 flex flex-col sm:flex-row sm:items-center gap-4">
        <BarChart3 className="w-10 h-10 text-[#a88fd8]" />
        <div>
          <h1 className="text-2xl sm:text-3xl font-semibold">AI Weekly Report</h1>
          <p className="text-gray-400 text-sm">{report.period}</p>
        </div>
      </div>

      {/* Summary Cards */}
      <div className="
        grid 
        grid-cols-1 
        sm:grid-cols-2 
        lg:grid-cols-4 
        gap-5 
        mb-10
      ">
        {[
          {
            title: "Campaigns Created",
            value: report.summary.campaigns_created,
            color: "from-[#4f46e5] to-[#818cf8]",
            icon: <Layers className="w-7 h-7" />,
          },
          {
            title: "Ads Generated",
            value: report.summary.ads_generated,
            color: "from-[#059669] to-[#34d399]",
            icon: <Zap className="w-7 h-7" />,
          },
          {
            title: "Images Generated",
            value: report.summary.images_generated,
            color: "from-[#9333ea] to-[#c084fc]",
            icon: <Lightbulb className="w-7 h-7" />,
          },
          {
            title: "Total Engagement",
            value: report.summary.total_engagement.toLocaleString(),
            sub: report.summary.engagement_growth,
            color: "from-[#f97316] to-[#fb923c]",
            icon: <TrendingUp className="w-7 h-7" />,
          },
        ].map((card, i) => (
          <div
            key={i}
            className="p-6 rounded-2xl bg-[#16111d]/70 border border-[#2a2235] hover:border-[#a88fd8]/40 transition-all shadow-md hover:shadow-[#a88fd8]/20"
          >
            <div className="flex justify-between items-start">
              <div className="flex-1 min-w-0">
                <p className="text-gray-400 text-sm truncate">{card.title}</p>
                <p className="text-3xl font-extrabold">{card.value}</p>
                {card.sub && (
                  <p className="text-sm text-green-400 mt-1">{card.sub}</p>
                )}
              </div>
              <div
                className={`p-3 rounded-full bg-gradient-to-br ${card.color} text-white shadow-md flex-shrink-0 ml-4`}
              >
                {card.icon}
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Key Insights */}
      <div className="bg-[#16111d]/70 border border-[#2a2235] rounded-2xl p-6 sm:p-8 mb-10 shadow-md">
        <h2 className="text-xl sm:text-2xl font-semibold mb-6 flex items-center gap-2 text-[#d9d3e8]">
          <Lightbulb className="w-6 h-6 text-[#a88fd8]" /> Key Insights This Week
        </h2>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
          {[
            { label: "Top Performing Platform", value: report.insights.top_performing_platform },
            { label: "Best Time to Post", value: report.insights.best_performing_time },
            { label: "Top Content Type", value: report.insights.highest_engagement_content },
            { label: "Audience Growth", value: report.insights.audience_growth },
          ].map((insight, i) => (
            <div
              key={i}
              className="bg-[#0f0c12]/70 border border-[#2a2235] rounded-xl p-5 hover:border-[#a88fd8]/40 transition-all"
            >
              <p className="text-sm text-gray-400 mb-1">{insight.label}</p>
              <p className="text-xl font-semibold">{insight.value}</p>
            </div>
          ))}
        </div>
      </div>

      {/* AI Recommendations */}
      <div className="bg-[#16111d]/70 border border-[#2a2235] rounded-2xl p-6 sm:p-8 mb-10 shadow-md">
        <h2 className="text-xl sm:text-2xl font-semibold mb-6 flex items-center gap-2 text-[#d9d3e8]">
          <Target className="w-6 h-6 text-[#a88fd8]" /> AI-Powered Recommendations
        </h2>

        <div className="space-y-5">
          {report.recommendations.map((rec, i) => (
            <div
              key={i}
              className="bg-[#0f0c12]/70 border border-[#2a2235] rounded-xl p-5 hover:border-[#a88fd8]/40 transition-all"
            >
              <div className="flex flex-col sm:flex-row gap-5">

                {/* Left Icon */}
                <div
                  className={`w-12 h-12 flex-shrink-0 rounded-lg flex items-center justify-center text-white ${
                    rec.priority === "high"
                      ? "bg-red-600/40"
                      : rec.priority === "medium"
                      ? "bg-yellow-500/30"
                      : "bg-blue-600/30"
                  }`}
                >
                  {rec.category === "Performance" && <TrendingUp />}
                  {rec.category === "Timing" && <Clock />}
                  {rec.category === "Audience" && <BarChart3 />}
                  {rec.category === "Content" && <Lightbulb />}
                </div>

                {/* Right Content */}
                <div className="flex-1 min-w-0">
                  <div className="flex flex-wrap items-center gap-3 mb-2">
                    <h3 className="text-lg font-semibold break-words">{rec.title}</h3>

                    <span
                      className={`px-3 py-1 rounded-full text-xs font-semibold uppercase whitespace-nowrap ${
                        rec.priority === "high"
                          ? "bg-red-500/20 text-red-400"
                          : rec.priority === "medium"
                          ? "bg-yellow-500/20 text-yellow-400"
                          : "bg-blue-500/20 text-blue-400"
                      }`}
                    >
                      {rec.priority} Priority
                    </span>
                  </div>

                  <p className="text-gray-400 mb-3">{rec.description}</p>

                  <div className="flex flex-wrap items-center gap-4">
                    <button className="px-4 py-2 rounded-lg bg-gradient-to-r from-[#3a3440] to-[#a88fd8] hover:brightness-110 transition text-sm">
                      {rec.action}
                    </button>

                    <span className="text-sm text-green-400 flex items-center gap-1">
                      <TrendingUp className="w-4 h-4" />
                      {rec.impact}
                    </span>
                  </div>
                </div>

              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Action Plan */}
      <div className="bg-[#16111d]/70 border border-[#2a2235] rounded-2xl p-6 sm:p-8 shadow-md">
        <h2 className="text-xl sm:text-2xl font-semibold mb-6 flex items-center gap-2 text-[#d9d3e8]">
          <CheckCircle className="w-6 h-6 text-[#a88fd8]" /> Your Action Plan for Next Week
        </h2>

        <div className="space-y-4">
          {report.next_steps.map((step, i) => (
            <div
              key={i}
              className="flex items-start gap-3 p-4 bg-[#0f0c12]/70 border border-[#2a2235] rounded-lg hover:border-[#a88fd8]/40 transition"
            >
              <div className="flex-shrink-0 w-7 h-7 rounded-full bg-gradient-to-r from-[#3a3440] to-[#a88fd8] flex items-center justify-center text-white text-sm font-semibold">
                {i + 1}
              </div>
              <p className="text-gray-300">{step}</p>
            </div>
          ))}
        </div>
      </div>

      {/* Export Button */}
      <div className="mt-10 flex justify-center">
        <button
          onClick={() => toast.success("PDF export coming soon!")}
          className="px-6 py-3 rounded-lg bg-gradient-to-r from-[#3a3440] to-[#a88fd8] text-white flex items-center gap-2 hover:brightness-110 transition shadow-lg"
        >
          <Download className="w-5 h-5" />
          Export Report as PDF
        </button>
      </div>

    </div>
  );
}
