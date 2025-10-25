import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Progress } from '@/components/ui/progress';
import { Alert, AlertDescription } from '@/components/ui/alert';
import {
  MessageSquare,
  GitCompare,
  BarChart3,
  FileText,
  AlertTriangle,
  CheckCircle,
  Info,
  Zap,
  Building,
  Calendar,
  DollarSign,
  Shield,
  Scale
} from 'lucide-react';

interface AdvancedAnalysisDashboardProps {
  contractId: string;
  analysisData: any;
}

const AdvancedAnalysisDashboard: React.FC<AdvancedAnalysisDashboardProps> = ({ contractId, analysisData }) => {
  const [activeTab, setActiveTab] = useState('overview');
  const [chatQuestion, setChatQuestion] = useState('');
  const [chatResponse, setChatResponse] = useState(null);
  const [comparisonResult, setComparisonResult] = useState(null);
  const [analyticsData, setAnalyticsData] = useState(null);

  // Enhanced risk color mapping
  const getRiskColor = (riskLevel: string) => {
    const colors = {
      'low': 'bg-green-100 text-green-800 border-green-200',
      'medium': 'bg-yellow-100 text-yellow-800 border-yellow-200',
      'high': 'bg-red-100 text-red-800 border-red-200',
      'critical': 'bg-purple-100 text-purple-800 border-purple-200'
    };
    return colors[riskLevel as keyof typeof colors] || 'bg-gray-100 text-gray-800 border-gray-200';
  };

  // Enhanced risk icons
  const getRiskIcon = (riskLevel: string) => {
    const icons = {
      'low': <CheckCircle className="h-4 w-4" />,
      'medium': <Info className="h-4 w-4" />,
      'high': <AlertTriangle className="h-4 w-4" />,
      'critical': <AlertTriangle className="h-4 w-4" />
    };
    return icons[riskLevel as keyof typeof icons] || <Info className="h-4 w-4" />;
  };

  const handleChatSubmit = async (e) => {
    e.preventDefault();
    if (!chatQuestion.trim()) return;

    try {
      const response = await fetch('/api/v1/analysis/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          contract_text: analysisData.extracted_text || '',
          question: chatQuestion,
          contract_context: analysisData.document_classification
        })
      });

      const result = await response.json();
      setChatResponse(result);
    } catch (error) {
      console.error('Chat error:', error);
      setChatResponse({
        answer: 'Unable to process question at this time.',
        confidence: 'low'
      });
    }
  };

  const handleComparison = async (otherContractId) => {
    try {
      const response = await fetch('/api/v1/analysis/compare-contracts', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          contract1_id: contractId,
          contract2_id: otherContractId,
          comparison_type: 'comprehensive'
        })
      });

      const result = await response.json();
      setComparisonResult(result);
    } catch (error) {
      console.error('Comparison error:', error);
    }
  };

  const loadAnalytics = async () => {
    try {
      const response = await fetch('/api/v1/analysis/analytics/dashboard');
      const result = await response.json();
      setAnalyticsData(result);
    } catch (error) {
      console.error('Analytics error:', error);
    }
  };

  useEffect(() => {
    loadAnalytics();
  }, []);

  return (
    <div className="max-w-7xl mx-auto p-6 space-y-6">
      {/* Enhanced Header */}
      <div className="bg-gradient-to-r from-blue-600 via-purple-600 to-indigo-600 rounded-xl p-6 text-white">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold mb-2">Advanced Contract Analysis</h1>
            <p className="text-blue-100 mb-4">
              Powered by Gemini 1.5 Flash with native PDF understanding
            </p>
            <div className="flex items-center space-x-6">
              <div className="text-center">
                <div className="text-2xl font-bold">{analysisData?.total_clauses || 0}</div>
                <div className="text-sm text-blue-100">Total Clauses</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold">{analysisData?.overall_risk_score?.toFixed(1) || 'N/A'}</div>
                <div className="text-sm text-blue-100">Risk Score</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold">{analysisData?.analysis_metadata?.processing_time_seconds?.toFixed(1) || 'N/A'}s</div>
                <div className="text-sm text-blue-100">Processing Time</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold">{analysisData?.analysis_metadata?.analysis_confidence?.toFixed(1) || 'N/A'}</div>
                <div className="text-sm text-blue-100">AI Confidence</div>
              </div>
            </div>
          </div>
          <div className="text-right">
            <Badge className="mb-2 bg-white/20 text-white border-white/30">
              <Zap className="h-3 w-3 mr-1" />
              Gemini 1.5 Flash
            </Badge>
            <div className="text-sm text-blue-100">
              Analysis Date: {new Date(analysisData?.analysis_date).toLocaleDateString()}
            </div>
          </div>
        </div>
      </div>

      {/* Enhanced Tabs */}
      <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
        <TabsList className="grid w-full grid-cols-6">
          <TabsTrigger value="overview" className="flex items-center space-x-2">
            <FileText className="h-4 w-4" />
            <span>Overview</span>
          </TabsTrigger>
          <TabsTrigger value="clauses" className="flex items-center space-x-2">
            <Scale className="h-4 w-4" />
            <span>Clauses</span>
          </TabsTrigger>
          <TabsTrigger value="chat" className="flex items-center space-x-2">
            <MessageSquare className="h-4 w-4" />
            <span>AI Chat</span>
          </TabsTrigger>
          <TabsTrigger value="comparison" className="flex items-center space-x-2">
            <GitCompare className="h-4 w-4" />
            <span>Compare</span>
          </TabsTrigger>
          <TabsTrigger value="analytics" className="flex items-center space-x-2">
            <BarChart3 className="h-4 w-4" />
            <span>Analytics</span>
          </TabsTrigger>
          <TabsTrigger value="structured" className="flex items-center space-x-2">
            <Building className="h-4 w-4" />
            <span>Structured Data</span>
          </TabsTrigger>
        </TabsList>

        {/* Overview Tab */}
        <TabsContent value="overview" className="space-y-6">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Document Classification */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <Building className="h-5 w-5" />
                  <span>Document Classification</span>
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="text-sm font-medium text-gray-500">Document Type</label>
                    <p className="text-lg font-semibold">
                      {analysisData?.document_classification?.document_type || 'Unknown'}
                    </p>
                  </div>
                  <div>
                    <label className="text-sm font-medium text-gray-500">Industry</label>
                    <p className="text-lg font-semibold">
                      {analysisData?.document_classification?.industry || 'General'}
                    </p>
                  </div>
                  <div>
                    <label className="text-sm font-medium text-gray-500">Jurisdiction</label>
                    <p className="text-lg font-semibold">
                      {analysisData?.document_classification?.jurisdiction || 'Unknown'}
                    </p>
                  </div>
                  <div>
                    <label className="text-sm font-medium text-gray-500">Parties</label>
                    <p className="text-sm">
                      {analysisData?.document_classification?.parties?.join(', ') || 'Not identified'}
                    </p>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Risk Analysis */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <AlertTriangle className="h-5 w-5" />
                  <span>Risk Analysis</span>
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="space-y-3">
                  {Object.entries(analysisData?.risk_summary || {}).map(([level, count]) => (
                    <div key={level} className="flex items-center justify-between">
                      <div className="flex items-center space-x-2">
                        {getRiskIcon(level)}
                        <span className="capitalize font-medium">{level} Risk</span>
                      </div>
                      <div className="flex items-center space-x-2">
                        <div className="w-20 bg-gray-200 rounded-full h-2">
                          <div
                            className={`h-2 rounded-full ${
                              level === 'low' ? 'bg-green-500' :
                              level === 'medium' ? 'bg-yellow-500' :
                              level === 'high' ? 'bg-red-500' : 'bg-purple-500'
                            }`}
                            style={{
                              width: `${(count / Math.max(analysisData?.total_clauses || 1, 1)) * 100}%`
                            }}
                          />
                        </div>
                        <span className="text-sm font-medium w-8">{count}</span>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Compliance Analysis */}
          {analysisData?.compliance_analysis && (
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <Shield className="h-5 w-5" />
                  <span>Compliance Analysis</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <div>
                    <label className="text-sm font-medium text-gray-500">Compliance Score</label>
                    <div className="flex items-center space-x-2">
                      <Progress
                        value={analysisData.compliance_analysis.compliance_score || 0}
                        className="flex-1"
                      />
                      <span className="text-lg font-semibold">
                        {analysisData.compliance_analysis.compliance_score || 0}/10
                      </span>
                    </div>
                  </div>
                  <div>
                    <label className="text-sm font-medium text-gray-500">Regulatory Framework</label>
                    <div className="flex flex-wrap gap-1">
                      {analysisData.compliance_analysis.regulatory_framework?.map((framework, index) => (
                        <Badge key={index} variant="outline" className="text-xs">
                          {framework}
                        </Badge>
                      )) || <span className="text-sm text-gray-500">None detected</span>}
                    </div>
                  </div>
                  <div>
                    <label className="text-sm font-medium text-gray-500">Issues Found</label>
                    <p className="text-sm">
                      {analysisData.compliance_analysis.compliance_issues?.length || 0} issues
                    </p>
                  </div>
                </div>
              </CardContent>
            </Card>
          )}

          {/* Key Insights */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <Info className="h-5 w-5" />
                <span>Key Insights</span>
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid gap-3">
                {analysisData?.key_insights?.map((insight, index) => (
                  <Alert key={index}>
                    <Info className="h-4 w-4" />
                    <AlertDescription>{insight}</AlertDescription>
                  </Alert>
                )) || <p className="text-gray-500">No insights available</p>}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Clauses Tab */}
        <TabsContent value="clauses" className="space-y-4">
          <div className="grid gap-4">
            {analysisData?.clauses?.map((clause, index) => (
              <Card key={index} className="hover:shadow-md transition-shadow">
                <CardHeader className="pb-3">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-3">
                      <CardTitle className="text-lg">
                        {clause.clause_type.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())}
                      </CardTitle>
                      <div className="flex items-center space-x-2">
                        {getRiskIcon(clause.risk_level)}
                        <Badge className={getRiskColor(clause.risk_level)}>
                          {clause.risk_level.charAt(0).toUpperCase() + clause.risk_level.slice(1)} Risk
                        </Badge>
                        <Badge variant="outline">
                          Score: {clause.risk_score}/10
                        </Badge>
                      </div>
                    </div>
                    <div className="text-sm text-gray-500">
                      Page {clause.page_number || 'N/A'}
                    </div>
                  </div>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div>
                    <h4 className="font-medium text-gray-900 mb-2">Clause Text:</h4>
                    <p className="text-gray-600 text-sm bg-gray-50 p-3 rounded">
                      {clause.clause_text}
                    </p>
                  </div>

                  {clause.simplified_explanation && (
                    <div>
                      <h4 className="font-medium text-gray-900 mb-2">Simplified Explanation:</h4>
                      <p className="text-gray-600 text-sm">
                        {clause.simplified_explanation}
                      </p>
                    </div>
                  )}

                  {clause.legal_implications && clause.legal_implications.length > 0 && (
                    <div>
                      <h4 className="font-medium text-gray-900 mb-2">Legal Implications:</h4>
                      <ul className="list-disc list-inside space-y-1">
                        {clause.legal_implications.map((implication, idx) => (
                          <li key={idx} className="text-sm text-gray-600">
                            {implication}
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}

                  {clause.recommendations && clause.recommendations.length > 0 && (
                    <div>
                      <h4 className="font-medium text-gray-900 mb-2">Recommendations:</h4>
                      <ul className="list-disc list-inside space-y-1">
                        {clause.recommendations.map((rec, idx) => (
                          <li key={idx} className="text-sm text-gray-600">
                            {rec}
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}
                </CardContent>
              </Card>
            )) || <p className="text-gray-500 text-center py-8">No clauses analyzed yet</p>}
          </div>
        </TabsContent>

        {/* Chat Tab */}
        <TabsContent value="chat" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <MessageSquare className="h-5 w-5" />
                <span>Ask LegalEase AI</span>
              </CardTitle>
              <CardDescription>
                Ask questions about this contract using contextual AI understanding
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <form onSubmit={handleChatSubmit} className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Your Question
                  </label>
                  <textarea
                    value={chatQuestion}
                    onChange={(e) => setChatQuestion(e.target.value)}
                    placeholder="Ask anything about this contract..."
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    rows={3}
                  />
                </div>
                <Button type="submit" className="w-full">
                  Ask AI Assistant
                </Button>
              </form>

              {chatResponse && (
                <div className="space-y-4">
                  <div className="bg-blue-50 p-4 rounded-lg">
                    <h4 className="font-medium text-gray-900 mb-2">AI Answer:</h4>
                    <p className="text-gray-700">{chatResponse.answer}</p>
                  </div>

                  {chatResponse.supporting_clauses && chatResponse.supporting_clauses.length > 0 && (
                    <div className="bg-green-50 p-4 rounded-lg">
                      <h4 className="font-medium text-gray-900 mb-2">Supporting Clauses:</h4>
                      <ul className="list-disc list-inside space-y-1">
                        {chatResponse.supporting_clauses.map((clause, idx) => (
                          <li key={idx} className="text-sm text-gray-600">{clause}</li>
                        ))}
                      </ul>
                    </div>
                  )}

                  {chatResponse.risks_concerns && chatResponse.risks_concerns.length > 0 && (
                    <div className="bg-red-50 p-4 rounded-lg">
                      <h4 className="font-medium text-gray-900 mb-2">Risks & Concerns:</h4>
                      <ul className="list-disc list-inside space-y-1">
                        {chatResponse.risks_concerns.map((risk, idx) => (
                          <li key={idx} className="text-sm text-gray-600">{risk}</li>
                        ))}
                      </ul>
                    </div>
                  )}

                  <div className="flex items-center justify-between">
                    <Badge variant="outline" className={
                      chatResponse.confidence === 'high' ? 'bg-green-100 text-green-800' :
                      chatResponse.confidence === 'medium' ? 'bg-yellow-100 text-yellow-800' :
                      'bg-red-100 text-red-800'
                    }>
                      Confidence: {chatResponse.confidence}
                    </Badge>
                  </div>
                </div>
              )}
            </CardContent>
          </Card>
        </TabsContent>

        {/* Comparison Tab */}
        <TabsContent value="comparison" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <GitCompare className="h-5 w-5" />
                <span>Compare Contracts</span>
              </CardTitle>
              <CardDescription>
                Compare this contract with another contract to identify differences and risk changes
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex space-x-4">
                <div className="flex-1">
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Compare with Contract ID
                  </label>
                  <input
                    type="text"
                    placeholder="Enter contract ID to compare..."
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    onKeyPress={(e) => {
                      if (e.key === 'Enter') {
                        handleComparison(e.target.value);
                      }
                    }}
                  />
                </div>
                <div className="flex items-end">
                  <Button onClick={() => handleComparison(document.querySelector('input[placeholder*="contract ID"]').value)}>
                    Compare
                  </Button>
                </div>
              </div>

              {comparisonResult && (
                <div className="space-y-6">
                  <Alert>
                    <AlertTriangle className="h-4 w-4" />
                    <AlertDescription>
                      {comparisonResult.comparison_summary}
                    </AlertDescription>
                  </Alert>

                  {comparisonResult.clause_differences && comparisonResult.clause_differences.length > 0 && (
                    <div>
                      <h4 className="font-medium text-gray-900 mb-3">Clause Differences:</h4>
                      <div className="space-y-3">
                        {comparisonResult.clause_differences.map((diff, index) => (
                          <Card key={index}>
                            <CardContent className="pt-4">
                              <div className="flex items-center space-x-2 mb-2">
                                <Badge variant="outline">{diff.clause_type}</Badge>
                                <Badge className={
                                  diff.risk_impact === 'higher' ? 'bg-red-100 text-red-800' :
                                  diff.risk_impact === 'lower' ? 'bg-green-100 text-green-800' :
                                  'bg-gray-100 text-gray-800'
                                }>
                                  Risk: {diff.risk_impact}
                                </Badge>
                              </div>
                              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
                                <div>
                                  <h5 className="font-medium mb-1">Contract 1:</h5>
                                  <p className="text-gray-600 bg-gray-50 p-2 rounded">
                                    {diff.contract1_version}
                                  </p>
                                </div>
                                <div>
                                  <h5 className="font-medium mb-1">Contract 2:</h5>
                                  <p className="text-gray-600 bg-gray-50 p-2 rounded">
                                    {diff.contract2_version}
                                  </p>
                                </div>
                              </div>
                            </CardContent>
                          </Card>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              )}
            </CardContent>
          </Card>
        </TabsContent>

        {/* Analytics Tab */}
        <TabsContent value="analytics" className="space-y-4">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Risk Distribution */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <BarChart3 className="h-5 w-5" />
                  <span>Risk Distribution</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                {analyticsData?.dashboard_data ? (
                  <div className="space-y-4">
                    {Object.entries(analyticsData.dashboard_data.risk_distribution).map(([level, count]) => (
                      <div key={level} className="flex items-center justify-between">
                        <div className="flex items-center space-x-2">
                          {getRiskIcon(level)}
                          <span className="capitalize font-medium">{level} Risk</span>
                        </div>
                        <div className="flex items-center space-x-2">
                          <div className="w-24 bg-gray-200 rounded-full h-2">
                            <div
                              className={`h-2 rounded-full ${
                                level === 'low' ? 'bg-green-500' :
                                level === 'medium' ? 'bg-yellow-500' :
                                level === 'high' ? 'bg-red-500' : 'bg-purple-500'
                              }`}
                              style={{
                                width: `${analyticsData.dashboard_data.total_contracts > 0 ?
                                  (count / (analyticsData.dashboard_data.total_contracts * 5)) * 100 : 0}%`
                              }}
                            />
                          </div>
                          <span className="text-sm font-medium w-8">{count}</span>
                        </div>
                      </div>
                    ))}
                  </div>
                ) : (
                  <p className="text-gray-500">Loading analytics...</p>
                )}
              </CardContent>
            </Card>

            {/* Top Clause Types */}
            <Card>
              <CardHeader>
                <CardTitle>Most Common Clause Types</CardTitle>
              </CardHeader>
              <CardContent>
                {analyticsData?.dashboard_data?.top_clause_types ? (
                  <div className="space-y-3">
                    {Object.entries(analyticsData.dashboard_data.top_clause_types).slice(0, 10).map(([type, count]) => (
                      <div key={type} className="flex items-center justify-between">
                        <span className="text-sm font-medium">
                          {type.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())}
                        </span>
                        <div className="flex items-center space-x-2">
                          <div className="w-20 bg-gray-200 rounded-full h-2">
                            <div
                              className="h-2 rounded-full bg-blue-500"
                              style={{
                                width: `${analyticsData.dashboard_data.total_contracts > 0 ?
                                  (count / Math.max(...Object.values(analyticsData.dashboard_data.top_clause_types))) * 100 : 0}%`
                              }}
                            />
                          </div>
                          <span className="text-sm font-medium w-8">{count}</span>
                        </div>
                      </div>
                    ))}
                  </div>
                ) : (
                  <p className="text-gray-500">Loading clause statistics...</p>
                )}
              </CardContent>
            </Card>
          </div>

          {/* Insights and Recommendations */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <Info className="h-5 w-5" />
                  <span>Portfolio Insights</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {analyticsData?.insights?.map((insight, index) => (
                    <Alert key={index}>
                      <Info className="h-4 w-4" />
                      <AlertDescription>{insight}</AlertDescription>
                    </Alert>
                  )) || <p className="text-gray-500">No insights available</p>}
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <CheckCircle className="h-5 w-5" />
                  <span>Recommendations</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {analyticsData?.recommendations?.map((rec, index) => (
                    <Alert key={index}>
                      <CheckCircle className="h-4 w-4" />
                      <AlertDescription>{rec}</AlertDescription>
                    </Alert>
                  )) || <p className="text-gray-500">No recommendations available</p>}
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        {/* Structured Data Tab */}
        <TabsContent value="structured" className="space-y-4">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Financial Data */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <DollarSign className="h-5 w-5" />
                  <span>Financial Terms</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div>
                    <label className="text-sm font-medium text-gray-500">Monetary Amounts</label>
                    <div className="space-y-2">
                      {/* This would be populated from the structured data extraction */}
                      <p className="text-sm text-gray-600">No financial data extracted yet</p>
                    </div>
                  </div>
                  <div>
                    <label className="text-sm font-medium text-gray-500">Payment Schedule</label>
                    <p className="text-sm text-gray-600">No payment schedule data available</p>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Temporal Data */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <Calendar className="h-5 w-5" />
                  <span>Important Dates</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div>
                    <label className="text-sm font-medium text-gray-500">Effective Dates</label>
                    <p className="text-sm text-gray-600">
                      {analysisData?.document_classification?.key_dates?.join(', ') || 'Not identified'}
                    </p>
                  </div>
                  <div>
                    <label className="text-sm font-medium text-gray-500">Contract Duration</label>
                    <p className="text-sm text-gray-600">
                      {analysisData?.document_classification?.duration || 'Not specified'}
                    </p>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Party Information */}
          <Card>
            <CardHeader>
              <CardTitle>Party Information</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label className="text-sm font-medium text-gray-500">Primary Parties</label>
                  <div className="space-y-2">
                    {analysisData?.document_classification?.parties?.map((party, index) => (
                      <Badge key={index} variant="outline" className="mr-2">
                        {party}
                      </Badge>
                    )) || <p className="text-sm text-gray-600">No parties identified</p>}
                  </div>
                </div>
                <div>
                  <label className="text-sm font-medium text-gray-500">Jurisdiction</label>
                  <p className="text-lg font-semibold">
                    {analysisData?.document_classification?.jurisdiction || 'Not specified'}
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
};

export default AdvancedAnalysisDashboard;
