"use client";

import { useQuery } from "@tanstack/react-query";
import axios from "axios";
import { Activity, Clock, Users, Globe } from "lucide-react";
import DashboardHeader from "@/components/DashboardHeader";
import KpiCard from "@/components/KpiCard";
import TrafficChart, { TrafficDataPoint } from "@/components/TrafficChart";
import OsChart, { OsDataPoint } from "@/components/OsChart";

interface EventBucket {
  bucket: string;
  operating_system?: string;
  page: string;
  avg_duration: number;
  count: number;
}

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/events/";
const API_KEY = process.env.NEXT_PUBLIC_API_KEY || "super_secret_api_key";

const fetchEvents = async (): Promise<EventBucket[]> => {
  const { data } = await axios.get<EventBucket[]>(API_URL, {
    headers: { "X-API-Key": API_KEY },
  });
  return data;
};

export default function Dashboard() {
  const { data, isLoading, error } = useQuery({
    queryKey: ["events"],
    queryFn: fetchEvents,
  });

  if (isLoading) return <div className="p-8 text-center text-gray-400">Loading analytics...</div>;
  if (error) return <div className="p-8 text-center text-red-400">Error loading data.</div>;

  // Process data for charts
  const timeSeriesData: TrafficDataPoint[] = data
    ? data.reduce((acc: TrafficDataPoint[], curr: EventBucket) => {
        const time = new Date(curr.bucket).toLocaleDateString();
        const existing = acc.find((item) => item.time === time);
        if (existing) {
          existing.views += curr.count;
        } else {
          acc.push({ time, views: curr.count });
        }
        return acc;
      }, [])
    : [];

  const sortedTimeSeriesData = [...timeSeriesData].sort(
    (a, b) => new Date(a.time).getTime() - new Date(b.time).getTime()
  );

  const osData: OsDataPoint[] = data
    ? data.reduce((acc: OsDataPoint[], curr: EventBucket) => {
        const os = curr.operating_system || "Unknown";
        const existing = acc.find((item) => item.name === os);
        if (existing) {
          existing.value += curr.count;
        } else {
          acc.push({ name: os, value: curr.count });
        }
        return acc;
      }, [])
    : [];

  const totalViews = data ? data.reduce((sum: number, curr: EventBucket) => sum + curr.count, 0) : 0;
  const avgDuration =
    data && data.length > 0
      ? data.reduce((sum: number, curr: EventBucket) => sum + (curr.avg_duration || 0), 0) / data.length
      : 0;

  return (
    <div className="min-h-screen bg-gray-950 p-8 font-sans">
      <div className="max-w-7xl mx-auto space-y-8">
        
        <DashboardHeader />

        {/* KPIs */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <KpiCard title="Total Page Views" value={totalViews} icon={<Activity className="w-6 h-6 text-blue-400" />} />
          <KpiCard title="Avg Session Duration" value={`${Math.round(avgDuration)}s`} icon={<Clock className="w-6 h-6 text-indigo-400" />} />
          <KpiCard title="Unique Visitors (est.)" value={Math.round(totalViews * 0.6)} icon={<Users className="w-6 h-6 text-emerald-400" />} />
          <KpiCard title="Top Region" value="US" icon={<Globe className="w-6 h-6 text-rose-400" />} />
        </div>

        {/* Charts Section */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="lg:col-span-2 h-full">
            <TrafficChart data={sortedTimeSeriesData} />
          </div>
          <div className="lg:col-span-1 h-full">
            <OsChart data={osData} />
          </div>
        </div>

      </div>
    </div>
  );
}
