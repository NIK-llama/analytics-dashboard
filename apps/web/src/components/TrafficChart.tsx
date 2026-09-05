"use client";

import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts";

export interface TrafficDataPoint {
  time: string;
  views: number;
}

export default function TrafficChart({ data }: { data: TrafficDataPoint[] }) {
  return (
    <div className="bg-gray-900 p-6 rounded-xl shadow-sm border border-gray-800">
      <h3 className="text-lg font-semibold text-gray-200 mb-6">Traffic Over Time</h3>
      <div className="h-80">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={data}>
            <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#374151" />
            <XAxis dataKey="time" axisLine={false} tickLine={false} tick={{fill: '#9CA3AF', fontSize: 12}} dy={10} />
            <YAxis axisLine={false} tickLine={false} tick={{fill: '#9CA3AF', fontSize: 12}} dx={-10} />
            <Tooltip 
              contentStyle={{backgroundColor: '#1F2937', color: '#fff', border: '1px solid #374151', borderRadius: '8px', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)'}}
              itemStyle={{color: '#60A5FA'}}
            />
            <Line 
              type="monotone" 
              dataKey="views" 
              stroke="#3B82F6" 
              strokeWidth={3} 
              dot={{r: 4, strokeWidth: 2, fill: '#1F2937', stroke: '#3B82F6'}}
              activeDot={{r: 6, strokeWidth: 0, fill: '#60A5FA'}}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
