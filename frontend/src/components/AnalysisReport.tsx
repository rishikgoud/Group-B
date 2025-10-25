import React from 'react';
import { PieChart, Pie, Cell, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

interface AnalysisReportProps {
  analysis: {
    analysis_id: string;
    contract_id: string;
    overall_risk_score: number;
    total_clauses: number;
    risk_summary: {
      high: number;
      medium: number;
      low: number;
    };
    clauses: Array<{
      clause_text: string;
      clause_type: string;
      risk_level: string;
      risk_score: number;
      simplified_explanation: string;
      recommendations: string[];
    }>;
    key_insights: string[];
    analysis_date: string;
    ai_model_used: string;
  };
}

const AnalysisReport: React.FC<AnalysisReportProps> = ({ analysis }) => {
  // Prepare data for charts
  const riskData = [
    { name: 'High Risk', value: analysis.risk_summary.high, color: '#ef4444' },
    { name: 'Medium Risk', value: analysis.risk_summary.medium, color: '#f59e0b' },
    { name: 'Low Risk', value: analysis.risk_summary.low, color: '#10b981' }
  ];

  // Clause type distribution
  const clauseTypeData = analysis.clauses.reduce((acc: any, clause) => {
    const type = clause.clause_type.replace('_', ' ').toUpperCase();
    acc[type] = (acc[type] || 0) + 1;
    return acc;
  }, {});

  const clauseTypeChartData = Object.entries(clauseTypeData).map(([type, count]) => ({
    type,
    count,
    percentage: ((count as number) / analysis.total_clauses * 100).toFixed(1)
  }));

  // Risk score distribution
  const riskScoreData = analysis.clauses.map((clause, index) => ({
    clause: `Clause ${index + 1}`,
    score: clause.risk_score,
    type: clause.clause_type.replace('_', ' ').toUpperCase()
  }));

  const getRiskColor = (level: string) => {
    switch (level) {
      case 'high': return '#ef4444';
      case 'medium': return '#f59e0b';
      case 'low': return '#10b981';
      default: return '#6b7280';
    }
  };

  const getRiskLevelColor = (score: number) => {
    if (score >= 8) return '#ef4444';
    if (score >= 5) return '#f59e0b';
    return '#10b981';
  };

  return (
    <div className="max-w-7xl mx-auto p-6 space-y-8">
      {/* Header */}
      <div className="bg-gradient-to-r from-blue-600 to-purple-600 rounded-xl p-6 text-white">
        <h1 className="text-3xl font-bold mb-2">Contract Analysis Report</h1>
        <p className="text-blue-100">
          Analyzed on {new Date(analysis.analysis_date).toLocaleDateString()} using {analysis.ai_model_used}
        </p>
        <div className="mt-4 flex items-center space-x-6">
          <div className="text-center">
            <div className="text-2xl font-bold">{analysis.total_clauses}</div>
            <div className="text-sm text-blue-100">Total Clauses</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold">{analysis.overall_risk_score.toFixed(1)}</div>
            <div className="text-sm text-blue-100">Overall Risk Score</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold">{analysis.risk_summary.high}</div>
            <div className="text-sm text-blue-100">High Risk Clauses</div>
          </div>
        </div>
      </div>

      {/* Risk Distribution Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Risk Level Pie Chart */}
        <div className="bg-white rounded-xl shadow-lg p-6">
          <h3 className="text-xl font-semibold mb-4 text-gray-800">Risk Level Distribution</h3>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={riskData}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, value, percent }) => `${name}: ${value} (${(percent * 100).toFixed(0)}%)`}
                outerRadius={80}
                fill="#8884d8"
                dataKey="value"
              >
                {riskData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>

        {/* Clause Type Distribution */}
        <div className="bg-white rounded-xl shadow-lg p-6">
          <h3 className="text-xl font-semibold mb-4 text-gray-800">Clause Type Distribution</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={clauseTypeChartData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="type" angle={-45} textAnchor="end" height={100} />
              <YAxis />
              <Tooltip />
              <Bar dataKey="count" fill="#3b82f6" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Risk Score Distribution */}
      <div className="bg-white rounded-xl shadow-lg p-6">
        <h3 className="text-xl font-semibold mb-4 text-gray-800">Risk Score by Clause</h3>
        <ResponsiveContainer width="100%" height={400}>
          <BarChart data={riskScoreData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="clause" />
            <YAxis domain={[0, 10]} />
            <Tooltip 
              formatter={(value: any, name: string, props: any) => [
                `${value}/10`,
                `${props.payload.type}`
              ]}
            />
            <Bar dataKey="score">
              {riskScoreData.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={getRiskLevelColor(entry.score)} />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>

      {/* Key Insights */}
      <div className="bg-white rounded-xl shadow-lg p-6">
        <h3 className="text-xl font-semibold mb-4 text-gray-800">Key Insights</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {analysis.key_insights.map((insight, index) => (
            <div key={index} className="flex items-start space-x-3 p-4 bg-blue-50 rounded-lg">
              <div className="w-6 h-6 bg-blue-500 rounded-full flex items-center justify-center text-white text-sm font-bold">
                {index + 1}
              </div>
              <p className="text-gray-700">{insight}</p>
            </div>
          ))}
        </div>
      </div>

      {/* Detailed Clauses */}
      <div className="bg-white rounded-xl shadow-lg p-6">
        <h3 className="text-xl font-semibold mb-4 text-gray-800">Detailed Clause Analysis</h3>
        <div className="space-y-4">
          {analysis.clauses.map((clause, index) => (
            <div key={index} className="border rounded-lg p-4 hover:shadow-md transition-shadow">
              <div className="flex items-start justify-between mb-3">
                <div className="flex items-center space-x-3">
                  <span className="px-3 py-1 bg-gray-100 rounded-full text-sm font-medium">
                    {clause.clause_type.replace('_', ' ').toUpperCase()}
                  </span>
                  <span 
                    className="px-3 py-1 rounded-full text-sm font-medium text-white"
                    style={{ backgroundColor: getRiskColor(clause.risk_level) }}
                  >
                    {clause.risk_level.toUpperCase()} RISK
                  </span>
                  <span className="text-sm text-gray-500">
                    Score: {clause.risk_score}/10
                  </span>
                </div>
              </div>
              
              <div className="mb-3">
                <h4 className="font-medium text-gray-800 mb-2">Clause Text:</h4>
                <p className="text-gray-600 text-sm bg-gray-50 p-3 rounded">
                  {clause.clause_text}
                </p>
              </div>
              
              <div className="mb-3">
                <h4 className="font-medium text-gray-800 mb-2">Simplified Explanation:</h4>
                <p className="text-gray-600 text-sm">
                  {clause.simplified_explanation}
                </p>
              </div>
              
              {clause.recommendations && clause.recommendations.length > 0 && (
                <div>
                  <h4 className="font-medium text-gray-800 mb-2">Recommendations:</h4>
                  <ul className="list-disc list-inside space-y-1">
                    {clause.recommendations.map((rec, recIndex) => (
                      <li key={recIndex} className="text-sm text-gray-600">
                        {rec}
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default AnalysisReport;
