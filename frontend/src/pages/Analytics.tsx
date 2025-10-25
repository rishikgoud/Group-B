import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, PieChart, Pie, Cell, ResponsiveContainer } from 'recharts';
import { TrendingUp, AlertTriangle, CheckCircle, Clock } from 'lucide-react';
import { useDatasetStats } from '../hooks/useAPI';

const Analytics: React.FC = () => {
  const { data: statsData, loading: statsLoading, error: statsError } = useDatasetStats();

  // Transform data for charts
  const riskData = statsData?.risk_level_distribution ? [
    { name: 'High Risk', value: statsData.risk_level_distribution.high || 0, color: '#ef4444' },
    { name: 'Medium Risk', value: statsData.risk_level_distribution.medium || 0, color: '#f59e0b' },
    { name: 'Low Risk', value: statsData.risk_level_distribution.low || 0, color: '#10b981' }
  ] : [];

  const clauseTypeData = statsData?.clause_type_distribution ? 
    Object.entries(statsData.clause_type_distribution).map(([name, count]) => ({
      name: name.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase()),
      count: count as number
    })) : [];

  const monthlyData = [
    { month: 'Jan', contracts: 4, riskScore: 6.2 },
    { month: 'Feb', contracts: 6, riskScore: 5.8 },
    { month: 'Mar', contracts: 8, riskScore: 6.5 },
    { month: 'Apr', contracts: 12, riskScore: 5.9 },
    { month: 'May', contracts: 15, riskScore: 6.1 },
    { month: 'Jun', contracts: 18, riskScore: 5.7 }
  ];

  return (
    <div className="max-w-7xl mx-auto">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Analytics Dashboard</h1>
        <p className="text-gray-600">Insights and trends from your contract analysis</p>
      </div>

      {statsLoading ? (
        <div className="text-center py-20">
          <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-500 text-lg">Loading analytics data...</p>
        </div>
      ) : statsError ? (
        <div className="text-center py-20">
          <AlertTriangle className="h-16 w-16 text-red-300 mx-auto mb-4" />
          <p className="text-red-500 text-lg">Failed to load analytics</p>
          <p className="text-gray-400">{statsError}</p>
        </div>
      ) : (
        <>
          {/* Key Metrics */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
            <div className="card text-center">
              <div className="bg-blue-100 w-12 h-12 rounded-full flex items-center justify-center mx-auto mb-3">
                <TrendingUp className="h-6 w-6 text-blue-600" />
              </div>
              <h3 className="text-2xl font-bold text-gray-900">{statsData?.total_clauses || 0}</h3>
              <p className="text-gray-600">Total Clauses</p>
              <p className="text-sm text-blue-600 mt-1">From Dataset</p>
            </div>

            <div className="card text-center">
              <div className="bg-red-100 w-12 h-12 rounded-full flex items-center justify-center mx-auto mb-3">
                <AlertTriangle className="h-6 w-6 text-red-600" />
              </div>
              <h3 className="text-2xl font-bold text-gray-900">{statsData?.risk_level_distribution?.high || 0}</h3>
              <p className="text-gray-600">High Risk Clauses</p>
              <p className="text-sm text-red-600 mt-1">Requires attention</p>
            </div>

            <div className="card text-center">
              <div className="bg-green-100 w-12 h-12 rounded-full flex items-center justify-center mx-auto mb-3">
                <CheckCircle className="h-6 w-6 text-green-600" />
              </div>
              <h3 className="text-2xl font-bold text-gray-900">{Object.keys(statsData?.clause_type_distribution || {}).length}</h3>
              <p className="text-gray-600">Clause Types</p>
              <p className="text-sm text-green-600 mt-1">Available</p>
            </div>

            <div className="card text-center">
              <div className="bg-purple-100 w-12 h-12 rounded-full flex items-center justify-center mx-auto mb-3">
                <Clock className="h-6 w-6 text-purple-600" />
              </div>
              <h3 className="text-2xl font-bold text-gray-900">2.3s</h3>
              <p className="text-gray-600">Avg Analysis Time</p>
              <p className="text-sm text-purple-600 mt-1">Lightning fast</p>
            </div>
          </div>

          {/* Charts Grid */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
            {/* Risk Distribution */}
            <div className="card">
              <h3 className="text-lg font-semibold mb-4">Risk Distribution</h3>
              {riskData.length > 0 ? (
                <ResponsiveContainer width="100%" height={300}>
                  <PieChart>
                    <Pie
                      data={riskData}
                      cx="50%"
                      cy="50%"
                      innerRadius={60}
                      outerRadius={100}
                      paddingAngle={5}
                      dataKey="value"
                    >
                      {riskData.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={entry.color} />
                      ))}
                    </Pie>
                    <Tooltip />
                  </PieChart>
                </ResponsiveContainer>
              ) : (
                <div className="text-center py-12 text-gray-500">
                  No risk data available
                </div>
              )}
              <div className="flex justify-center space-x-6 mt-4">
                {riskData.map((item, index) => (
                  <div key={index} className="flex items-center space-x-2">
                    <div 
                      className="w-3 h-3 rounded-full" 
                      style={{ backgroundColor: item.color }}
                    ></div>
                    <span className="text-sm text-gray-600">{item.name}</span>
                  </div>
                ))}
              </div>
            </div>

            {/* Clause Types */}
            <div className="card">
              <h3 className="text-lg font-semibold mb-4">Clause Types Analysis</h3>
              {clauseTypeData.length > 0 ? (
                <ResponsiveContainer width="100%" height={300}>
                  <BarChart data={clauseTypeData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis 
                      dataKey="name" 
                      angle={-45}
                      textAnchor="end"
                      height={80}
                      fontSize={12}
                    />
                    <YAxis />
                    <Tooltip />
                    <Bar dataKey="count" fill="#3b82f6" />
                  </BarChart>
                </ResponsiveContainer>
              ) : (
                <div className="text-center py-12 text-gray-500">
                  No clause type data available
                </div>
              )}
            </div>
          </div>
        </>
      )}

      {/* Monthly Trends */}
      <div className="card mb-8">
        <h3 className="text-lg font-semibold mb-4">Monthly Contract Analysis Trends</h3>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={monthlyData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="month" />
            <YAxis yAxisId="left" />
            <YAxis yAxisId="right" orientation="right" />
            <Tooltip />
            <Bar yAxisId="left" dataKey="contracts" fill="#3b82f6" name="Contracts Analyzed" />
            <Bar yAxisId="right" dataKey="riskScore" fill="#f59e0b" name="Avg Risk Score" />
          </BarChart>
        </ResponsiveContainer>
      </div>

      {/* Recent Activity */}
      <div className="card">
        <h3 className="text-lg font-semibold mb-4">Recent Analysis Activity</h3>
        <div className="space-y-3">
          <div className="flex items-center justify-between py-2 border-b border-gray-100">
            <div className="flex items-center space-x-3">
              <div className="w-2 h-2 bg-green-500 rounded-full"></div>
              <span className="text-sm">Employment Agreement - John Smith.pdf</span>
            </div>
            <div className="flex items-center space-x-2">
              <span className="risk-medium px-2 py-1 rounded-full text-xs">Medium Risk</span>
              <span className="text-xs text-gray-500">2 hours ago</span>
            </div>
          </div>
          
          <div className="flex items-center justify-between py-2 border-b border-gray-100">
            <div className="flex items-center space-x-3">
              <div className="w-2 h-2 bg-yellow-500 rounded-full"></div>
              <span className="text-sm">NDA Template.docx</span>
            </div>
            <div className="flex items-center space-x-2">
              <span className="risk-low px-2 py-1 rounded-full text-xs">Low Risk</span>
              <span className="text-xs text-gray-500">1 day ago</span>
            </div>
          </div>
          
          <div className="flex items-center justify-between py-2 border-b border-gray-100">
            <div className="flex items-center space-x-3">
              <div className="w-2 h-2 bg-red-500 rounded-full"></div>
              <span className="text-sm">Service Agreement - Vendor ABC.pdf</span>
            </div>
            <div className="flex items-center space-x-2">
              <span className="risk-high px-2 py-1 rounded-full text-xs">High Risk</span>
              <span className="text-xs text-gray-500">2 days ago</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Analytics;
