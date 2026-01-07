/**
 * Price distribution chart component.
 */

import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from 'recharts';

const PriceChart = ({ data }) => {
  // Transform data for chart
  const chartData = [];
  
  if (data && Object.keys(data).length > 0) {
    const priceRanges = {
      '0-10': 0,
      '10-25': 0,
      '25-50': 0,
      '50-100': 0,
      '100+': 0,
    };

    for (const [platform, products] of Object.entries(data)) {
      products.forEach((product) => {
        const price = product.price || 0;
        if (price < 10) priceRanges['0-10']++;
        else if (price < 25) priceRanges['10-25']++;
        else if (price < 50) priceRanges['25-50']++;
        else if (price < 100) priceRanges['50-100']++;
        else priceRanges['100+']++;
      });
    }

    Object.entries(priceRanges).forEach(([range, count]) => {
      chartData.push({ range: `RM ${range}`, count });
    });
  }

  if (chartData.length === 0) {
    return (
      <div className="text-center py-8 text-gray-500">
        <p>No data available for price chart</p>
      </div>
    );
  }

  return (
    <ResponsiveContainer width="100%" height={300}>
      <BarChart data={chartData}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="range" />
        <YAxis />
        <Tooltip />
        <Legend />
        <Bar dataKey="count" fill="#0ea5e9" name="Products" />
      </BarChart>
    </ResponsiveContainer>
  );
};

export default PriceChart;
