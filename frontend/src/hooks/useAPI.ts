/**
 * Custom hooks for API calls with loading states and error handling
 */

import { useState, useEffect, useCallback } from 'react';
import { contractAPI, analysisAPI, datasetAPI, healthAPI, handleAPIError } from '../services/api';

// Generic API hook
export const useAPI = <T>(
  apiCall: () => Promise<{ data: T }>,
  dependencies: any[] = []
) => {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const execute = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await apiCall();
      setData(response.data);
    } catch (err) {
      const errorInfo = handleAPIError(err);
      setError(errorInfo.message);
    } finally {
      setLoading(false);
    }
  }, dependencies);

  useEffect(() => {
    execute();
  }, [execute]);

  return { data, loading, error, refetch: execute };
};

// Contract hooks
export const useContracts = () => {
  return useAPI(() => contractAPI.list());
};

export const useContract = (contractId: string | null) => {
  return useAPI(
    () => contractAPI.getById(contractId!),
    [contractId]
  );
};

export const useContractUpload = () => {
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const uploadContract = async (file: File) => {
    setUploading(true);
    setError(null);
    try {
      const response = await contractAPI.upload(file);
      return response.data;
    } catch (err) {
      const errorInfo = handleAPIError(err);
      setError(errorInfo.message);
      throw err;
    } finally {
      setUploading(false);
    }
  };

  return { uploadContract, uploading, error };
};

// Analysis hooks
export const useContractAnalysis = (contractId: string | null) => {
  return useAPI(
    () => analysisAPI.analyze(contractId!),
    [contractId]
  );
};

export const useRiskLevels = () => {
  return useAPI(() => analysisAPI.getRiskLevels());
};

export const useClauseTypes = () => {
  return useAPI(() => analysisAPI.getClauseTypes());
};

// Dataset hooks
export const useDatasetClauses = (params: {
  clause_type?: string;
  risk_level?: string;
  search_text?: string;
  page?: number;
  page_size?: number;
} = {}) => {
  return useAPI(
    () => datasetAPI.getClauses(params),
    [params.clause_type, params.risk_level, params.search_text, params.page, params.page_size]
  );
};

export const useDatasetStats = () => {
  return useAPI(() => datasetAPI.getStats());
};

export const useDatasetClauseTypes = () => {
  return useAPI(() => datasetAPI.getClauseTypes());
};

export const useDatasetRiskLevels = () => {
  return useAPI(() => datasetAPI.getRiskLevels());
};

// Health check hook
export const useHealthCheck = () => {
  return useAPI(() => healthAPI.check());
};

// Utility hook for manual API calls
export const useManualAPI = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const execute = async <T>(apiCall: () => Promise<{ data: T }>) => {
    setLoading(true);
    setError(null);
    try {
      const response = await apiCall();
      return response.data;
    } catch (err) {
      const errorInfo = handleAPIError(err);
      setError(errorInfo.message);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  return { execute, loading, error };
};
