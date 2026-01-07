/**
 * Sales volume chart component.
 */

import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from 'recharts';

const SalesChart = ({ data }) => {
  // Group by platform and calculate total sales
  const platformSales = {};

  if (data && Object.keys(data).length > 0) {
    for (const [platform, products] of Object.entries(data)) {
      const totalSales = products.reduce((sum, product) => sum + (product.sold || 0), 0);
      const avgSales = products.length > 0 ? totalSales / products.length : 0;
      platformSales[platform] = {
        total: totalSales,
        average: Math.round(avgSales),
        count: products.length,
      };
    }
  }

  const chartData = Object.entries(platformSales).map(([platform, stats]) => ({
    platform: platform.charAt(0).toUpperCase() + platform.slice(1),
    total: stats.total,
    average: stats.average,
  }));

  if (chartData.length === 0) {
    return (
      <div className="text-center py-8 text-gray-500">
        <p>No data available for sales chart</p>
      </div>
    );
  }

  return (
    <ResponsiveContainer width="100%" height={300}>
      <BarChart data={chartData}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="platform" />
        <YAxis />
        <Tooltip />
        <Legend />
        <Bar dataKey="total" fill="#10b981" name="Total Sales" />
        <Bar dataKey="average" fill="#0ea5e9" name="Average Sales" />
      </BarChart>
    </ResponsiveContainer>
  );
};

export default SalesChart;
