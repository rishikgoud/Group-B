import React, { useState } from 'react';
import { Search, FileText, AlertTriangle } from 'lucide-react';
import { useDatasetClauses, useDatasetClauseTypes, useDatasetRiskLevels } from '../hooks/useAPI';

const DatasetExplorer: React.FC = () => {
  const [filters, setFilters] = useState({
    clause_type: '',
    risk_level: '',
    search_text: '',
    page: 1,
    page_size: 20
  });

  const { data: clausesData, loading: clausesLoading, error: clausesError } = useDatasetClauses(filters);
  const { data: clauseTypesData } = useDatasetClauseTypes();
  const { data: riskLevelsData } = useDatasetRiskLevels();

  const handleFilterChange = (key: string, value: string) => {
    setFilters(prev => ({
      ...prev,
      [key]: value,
      page: 1 // Reset to first page when filters change
    }));
  };

  const handlePageChange = (newPage: number) => {
    setFilters(prev => ({
      ...prev,
      page: newPage
    }));
  };

  const getRiskColor = (riskLevel: string) => {
    switch (riskLevel) {
      case 'high': return 'bg-red-100 text-red-800 border-red-200';
      case 'medium': return 'bg-yellow-100 text-yellow-800 border-yellow-200';
      case 'low': return 'bg-green-100 text-green-800 border-green-200';
      default: return 'bg-gray-100 text-gray-800 border-gray-200';
    }
  };

  return (
    <div className="max-w-7xl mx-auto">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Dataset Explorer</h1>
        <p className="text-gray-600">Explore legal clauses from the Kaggle Contracts Clauses Dataset</p>
      </div>

      {/* Filters */}
      <div className="card mb-8">
        <h2 className="text-xl font-semibold mb-4">Search & Filter</h2>
        
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          {/* Search */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Search Text
            </label>
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
              <input
                type="text"
                placeholder="Search in clause text..."
                value={filters.search_text}
                onChange={(e) => handleFilterChange('search_text', e.target.value)}
                className="w-full pl-10 pr-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
          </div>

          {/* Clause Type Filter */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Clause Type
            </label>
            <select
              value={filters.clause_type}
              onChange={(e) => handleFilterChange('clause_type', e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              <option value="">All Types</option>
              {clauseTypesData?.clause_types?.map((type: string) => (
                <option key={type} value={type}>
                  {type.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())}
                </option>
              ))}
            </select>
          </div>

          {/* Risk Level Filter */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Risk Level
            </label>
            <select
              value={filters.risk_level}
              onChange={(e) => handleFilterChange('risk_level', e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              <option value="">All Levels</option>
              {riskLevelsData?.risk_levels?.map((level: string) => (
                <option key={level} value={level}>
                  {level.charAt(0).toUpperCase() + level.slice(1)} Risk
                </option>
              ))}
            </select>
          </div>

          {/* Page Size */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Items per Page
            </label>
            <select
              value={filters.page_size}
              onChange={(e) => handleFilterChange('page_size', e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              <option value={10}>10</option>
              <option value={20}>20</option>
              <option value={50}>50</option>
              <option value={100}>100</option>
            </select>
          </div>
        </div>
      </div>

      {/* Results */}
      <div className="card">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-xl font-semibold">Clauses</h2>
          {clausesData && (
            <span className="text-sm text-gray-500">
              Showing {((filters.page - 1) * filters.page_size) + 1} - {Math.min(filters.page * filters.page_size, clausesData.total_count)} of {clausesData.total_count}
            </span>
          )}
        </div>

        {clausesLoading ? (
          <div className="text-center py-12">
            <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-blue-600 mx-auto mb-4"></div>
            <p className="text-gray-500 text-lg">Loading clauses...</p>
          </div>
        ) : clausesError ? (
          <div className="text-center py-12">
            <AlertTriangle className="h-16 w-16 text-red-300 mx-auto mb-4" />
            <p className="text-red-500 text-lg">Failed to load clauses</p>
            <p className="text-gray-400">{clausesError}</p>
          </div>
        ) : !clausesData?.clauses || clausesData.clauses.length === 0 ? (
          <div className="text-center py-12">
            <FileText className="h-16 w-16 text-gray-300 mx-auto mb-4" />
            <p className="text-gray-500 text-lg">No clauses found</p>
            <p className="text-gray-400">Try adjusting your search filters</p>
          </div>
        ) : (
          <>
            <div className="space-y-4">
              {clausesData.clauses.map((clause: any) => (
                <div key={clause.id} className="border border-gray-200 rounded-lg p-6 hover:shadow-md transition-shadow">
                  <div className="flex justify-between items-start mb-3">
                    <div className="flex items-center space-x-3">
                      <FileText className="h-6 w-6 text-blue-600" />
                      <div>
                        <h3 className="font-semibold text-lg">
                          {clause.clause_type.replace('_', ' ').replace(/\b\w/g, (l: string) => l.toUpperCase())}
                        </h3>
                        <p className="text-sm text-gray-500">
                          ID: {clause.id} • Added {new Date(clause.created_at).toLocaleDateString()}
                        </p>
                      </div>
                    </div>
                    {clause.risk_level && (
                      <span className={`px-3 py-1 rounded-full text-sm font-medium border ${getRiskColor(clause.risk_level)}`}>
                        {clause.risk_level.charAt(0).toUpperCase() + clause.risk_level.slice(1)} Risk
                      </span>
                    )}
                  </div>
                  
                  <div className="mb-4">
                    <h4 className="font-medium text-gray-900 mb-2">Original Text:</h4>
                    <p className="text-gray-700 bg-gray-50 p-3 rounded-lg text-sm leading-relaxed">
                      {clause.text}
                    </p>
                  </div>

                  {clause.simplified_text && (
                    <div>
                      <h4 className="font-medium text-gray-900 mb-2">Simplified Explanation:</h4>
                      <p className="text-gray-600 bg-blue-50 p-3 rounded-lg text-sm leading-relaxed">
                        {clause.simplified_text}
                      </p>
                    </div>
                  )}
                </div>
              ))}
            </div>

            {/* Pagination */}
            {clausesData.total_count > filters.page_size && (
              <div className="flex justify-center items-center space-x-2 mt-8">
                <button
                  onClick={() => handlePageChange(filters.page - 1)}
                  disabled={filters.page === 1}
                  className="px-3 py-2 border border-gray-300 rounded-lg disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-50"
                >
                  Previous
                </button>
                
                <span className="px-4 py-2 text-sm text-gray-600">
                  Page {filters.page} of {Math.ceil(clausesData.total_count / filters.page_size)}
                </span>
                
                <button
                  onClick={() => handlePageChange(filters.page + 1)}
                  disabled={filters.page >= Math.ceil(clausesData.total_count / filters.page_size)}
                  className="px-3 py-2 border border-gray-300 rounded-lg disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-50"
                >
                  Next
                </button>
              </div>
            )}
          </>
        )}
      </div>
    </div>
  );
};

export default DatasetExplorer;
