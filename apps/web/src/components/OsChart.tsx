"use client";

import { PieChart, Pie, Tooltip, ResponsiveContainer, Legend } from "recharts";

const COLORS = ['#3B82F6', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6', '#6B7280'];

export interface OsDataPoint {
  name: string;
  value: number;
  fill?: string;
}

export default function OsChart({ data }: { data: OsDataPoint[] }) {
  const dataWithColors = data.map((entry, index) => ({
    ...entry,
    fill: COLORS[index % COLORS.length]
  }));

  return (
    <div className="bg-gray-900 p-6 rounded-xl shadow-sm border border-gray-800 h-full">
      <h3 className="text-lg font-semibold text-gray-200 mb-6">Operating Systems</h3>
      <div className="h-80">
        <ResponsiveContainer width="100%" height="100%">
          <PieChart>
            <Pie
              data={dataWithColors}
              cx="50%"
              cy="50%"
              innerRadius={60}
              outerRadius={100}
              paddingAngle={5}
              dataKey="value"
              stroke="none"
            />
            <Tooltip 
              contentStyle={{backgroundColor: '#1F2937', color: '#fff', border: '1px solid #374151', borderRadius: '8px', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)'}}
              itemStyle={{color: '#E5E7EB'}}
            />
            <Legend position="bottom" height={36} wrapperStyle={{color: '#9CA3AF', paddingTop: '20px'}} />
          </PieChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
