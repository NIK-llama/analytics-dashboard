export default function KpiCard({ title, value, icon }: { title: string, value: string | number, icon: React.ReactNode }) {
  return (
    <div className="bg-gray-900 p-6 rounded-xl shadow-sm border border-gray-800 flex items-center space-x-4">
      <div className="p-3 bg-gray-800/50 rounded-lg">
        {icon}
      </div>
      <div>
        <p className="text-sm font-medium text-gray-400">{title}</p>
        <p className="text-2xl font-bold text-gray-100">{value}</p>
      </div>
    </div>
  );
}
