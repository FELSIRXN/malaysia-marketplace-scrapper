/**
 * Rating distribution chart component.
 */

import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip, Legend } from 'recharts';

const RatingChart = ({ data }) => {
  const ratingData = {
    '5 Stars': 0,
    '4-5 Stars': 0,
    '3-4 Stars': 0,
    '2-3 Stars': 0,
    '< 2 Stars': 0,
  };

  if (data && Object.keys(data).length > 0) {
    for (const [platform, products] of Object.entries(data)) {
      products.forEach((product) => {
        const rating = product.rating || 0;
        if (rating >= 5) ratingData['5 Stars']++;
        else if (rating >= 4) ratingData['4-5 Stars']++;
        else if (rating >= 3) ratingData['3-4 Stars']++;
        else if (rating >= 2) ratingData['2-3 Stars']++;
        else ratingData['< 2 Stars']++;
      });
    }
  }

  const chartData = Object.entries(ratingData)
    .filter(([_, count]) => count > 0)
    .map(([name, value]) => ({ name, value }));

  const COLORS = ['#0ea5e9', '#10b981', '#f59e0b', '#ef4444', '#6b7280'];

  if (chartData.length === 0) {
    return (
      <div className="text-center py-8 text-gray-500">
        <p>No data available for rating chart</p>
      </div>
    );
  }

  return (
    <ResponsiveContainer width="100%" height={300}>
      <PieChart>
        <Pie
          data={chartData}
          cx="50%"
          cy="50%"
          labelLine={false}
          label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
          outerRadius={80}
          fill="#8884d8"
          dataKey="value"
        >
          {chartData.map((entry, index) => (
            <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
          ))}
        </Pie>
        <Tooltip />
        <Legend />
      </PieChart>
    </ResponsiveContainer>
  );
};

export default RatingChart;
