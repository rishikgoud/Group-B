/**
 * API service for communicating with LegalEase AI backend
 */

import axios from 'axios';

// API configuration
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';
const API_VERSION = process.env.REACT_APP_API_VERSION || 'v1';

// Create axios instance
const api = axios.create({
  baseURL: `${API_BASE_URL}/api/${API_VERSION}`,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor
api.interceptors.request.use(
  (config) => {
    console.log(`🚀 API Request: ${config.method?.toUpperCase()} ${config.url}`);
    return config;
  },
  (error) => {
    console.error('❌ API Request Error:', error);
    return Promise.reject(error);
  }
);

// Response interceptor
api.interceptors.response.use(
  (response) => {
    console.log(`✅ API Response: ${response.status} ${response.config.url}`);
    return response;
  },
  (error) => {
    console.error('❌ API Response Error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

// Health Check API
export const healthAPI = {
  check: () => api.get('/health'),
  detailed: () => api.get('/health/detailed'),
};

// Contract API
export const contractAPI = {
  // Upload contract
  upload: (file: File) => {
    const formData = new FormData();
    formData.append('file', file);
    return api.post('/contracts/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  },

  // Get contracts list
  list: (skip = 0, limit = 100) => 
    api.get(`/contracts/list?skip=${skip}&limit=${limit}`),

  // Get contract by ID
  getById: (contractId: number) => 
    api.get(`/contracts/${contractId}`),

  // Delete contract
  delete: (contractId: number) => 
    api.delete(`/contracts/${contractId}`),
};

// Analysis API
export const analysisAPI = {
  // Analyze contract
  analyze: (contractId: number, analysisType = 'full') =>
    api.post('/analysis/analyze', {
      contract_id: contractId,
      analysis_type: analysisType,
    }),

  // Get risk levels
  getRiskLevels: () => api.get('/analysis/risk-levels'),

  // Get clause types
  getClauseTypes: () => api.get('/analysis/clause-types'),

  // Get contract analysis
  getContractAnalysis: (contractId: number) =>
    api.get(`/analysis/contract/${contractId}/analysis`),
};

// Dataset API
export const datasetAPI = {
  // Get clauses
  getClauses: (params: {
    clause_type?: string;
    risk_level?: string;
    search_text?: string;
    page?: number;
    page_size?: number;
  } = {}) => {
    const searchParams = new URLSearchParams();
    Object.entries(params).forEach(([key, value]) => {
      if (value !== undefined && value !== null) {
        searchParams.append(key, value.toString());
      }
    });
    return api.get(`/dataset/clauses?${searchParams.toString()}`);
  },

  // Get clause by ID
  getClauseById: (clauseId: number) =>
    api.get(`/dataset/clauses/${clauseId}`),

  // Get clause types
  getClauseTypes: () => api.get('/dataset/clauses/types/list'),

  // Get risk levels
  getRiskLevels: () => api.get('/dataset/clauses/risk-levels/list'),

  // Get dataset statistics
  getStats: () => api.get('/dataset/stats'),

  // Reload dataset
  reload: () => api.post('/dataset/reload'),
};

// Chat API (placeholder for future implementation)
export const chatAPI = {
  // Send message
  sendMessage: (message: string, sessionId?: string, contractId?: number) =>
    api.post('/chat/ask', {
      message,
      session_id: sessionId,
      contract_id: contractId,
    }),

  // Get suggestions
  getSuggestions: () => api.get('/chat/suggestions'),
};

// Error handling utility
export const handleAPIError = (error: any) => {
  if (error.response) {
    // Server responded with error status
    const { status, data } = error.response;
    return {
      message: data.detail || data.error || 'An error occurred',
      status,
      code: data.error_code,
    };
  } else if (error.request) {
    // Request was made but no response received
    return {
      message: 'Network error - please check your connection',
      status: 0,
      code: 'NETWORK_ERROR',
    };
  } else {
    // Something else happened
    return {
      message: error.message || 'An unexpected error occurred',
      status: -1,
      code: 'UNKNOWN_ERROR',
    };
  }
};

export default api;
