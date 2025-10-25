import React, { useState, useEffect } from 'react';
import { Upload, FileText, AlertTriangle, CheckCircle, Clock, Trash2, Brain, BarChart3 } from 'lucide-react';
import { useContracts, useContractUpload } from '../hooks/useAPI';
import { analysisAPI } from '../services/api';
import AnalysisLoading from '../components/AnalysisLoading';
import AnalysisReport from '../components/AnalysisReport';
import toast from 'react-hot-toast';

const Dashboard: React.FC = () => {
  const [dragActive, setDragActive] = useState(false);
  const [analyzing, setAnalyzing] = useState(false);
  const [analysisResult, setAnalysisResult] = useState<any>(null);
  const [selectedContract, setSelectedContract] = useState<string | null>(null);
  const { data: contractsData, loading: contractsLoading, error: contractsError, refetch: refetchContracts } = useContracts();
  const { uploadContract, uploading, error: uploadError } = useContractUpload();

  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFiles(e.dataTransfer.files);
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    e.preventDefault();
    if (e.target.files && e.target.files[0]) {
      handleFiles(e.target.files);
    }
  };

  const handleFiles = async (files: FileList) => {
    if (files.length === 0) return;
    
    const file = files[0]; // Handle single file for now
    
    try {
      const result = await uploadContract(file);
      toast.success(`Contract "${file.name}" uploaded successfully!`);
      refetchContracts(); // Refresh the contracts list
    } catch (error) {
      toast.error(`Failed to upload contract: ${error}`);
    }
  };

  const handleAnalyze = async (contractId: string) => {
    setAnalyzing(true);
    setSelectedContract(contractId);
    
    try {
      const response = await analysisAPI.analyze(contractId, 'full');
      setAnalysisResult(response.data);
      toast.success('Contract analysis completed successfully!');
    } catch (error: any) {
      toast.error(`Analysis failed: ${error.response?.data?.detail || error.message}`);
    } finally {
      setAnalyzing(false);
    }
  };

  const handleViewAnalysis = async (contractId: string) => {
    try {
      const response = await analysisAPI.getContractAnalysis(contractId);
      setAnalysisResult(response.data);
      setSelectedContract(contractId);
    } catch (error: any) {
      toast.error(`Failed to load analysis: ${error.response?.data?.detail || error.message}`);
    }
  };

  return (
    <div className="max-w-6xl mx-auto">
      {/* Analysis Loading Overlay */}
      <AnalysisLoading 
        isVisible={analyzing} 
        message="Analyzing contract with AI. This may take a few moments..."
      />
      
      {/* Analysis Report Modal */}
      {analysisResult && (
        <div className="fixed inset-0 z-50 bg-black bg-opacity-50 backdrop-blur-sm overflow-y-auto">
          <div className="min-h-screen flex items-center justify-center p-4">
            <div className="bg-white rounded-2xl shadow-2xl max-w-7xl w-full max-h-[90vh] overflow-y-auto">
              <div className="sticky top-0 bg-white border-b border-gray-200 p-4 flex justify-between items-center">
                <h2 className="text-2xl font-bold text-gray-900">Analysis Report</h2>
                <button 
                  onClick={() => setAnalysisResult(null)}
                  className="text-gray-500 hover:text-gray-700 text-2xl"
                >
                  ×
                </button>
              </div>
              <AnalysisReport analysis={analysisResult} />
            </div>
          </div>
        </div>
      )}

      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Contract Dashboard</h1>
        <p className="text-gray-600">Upload and analyze your contracts with AI-powered insights</p>
      </div>

      {/* Upload Section */}
      <div className="card mb-8">
        <h2 className="text-xl font-semibold mb-4">Upload New Contract</h2>
        
        <div
          className={`border-2 border-dashed rounded-lg p-8 text-center transition-colors duration-200 ${
            dragActive 
              ? 'border-blue-500 bg-blue-50' 
              : 'border-gray-300 hover:border-gray-400'
          } ${uploading ? 'opacity-50 pointer-events-none' : ''}`}
          onDragEnter={handleDrag}
          onDragLeave={handleDrag}
          onDragOver={handleDrag}
          onDrop={handleDrop}
        >
          {uploading ? (
            <div className="flex flex-col items-center">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mb-4"></div>
              <p className="text-lg font-medium text-gray-700 mb-2">Uploading contract...</p>
              <p className="text-gray-500">Please wait while we process your file</p>
            </div>
          ) : (
            <>
              <Upload className="h-12 w-12 text-gray-400 mx-auto mb-4" />
              <p className="text-lg font-medium text-gray-700 mb-2">
                Drag and drop your contract here
              </p>
              <p className="text-gray-500 mb-4">
                or click to browse files
              </p>
              <input
                type="file"
                multiple
                accept=".pdf,.docx,.txt,.png,.jpg,.jpeg"
                onChange={handleChange}
                className="hidden"
                id="file-upload"
                disabled={uploading}
              />
              <label
                htmlFor="file-upload"
                className="btn-primary cursor-pointer inline-block"
              >
                Choose Files
              </label>
              <p className="text-sm text-gray-400 mt-2">
                Supports PDF, DOCX, TXT, PNG, JPG, JPEG (Max 10MB)
              </p>
            </>
          )}
        </div>
      </div>

      {/* Recent Contracts */}
      <div className="card">
        <h2 className="text-xl font-semibold mb-4">Recent Contracts</h2>
        
        {contractsLoading ? (
          <div className="text-center py-12">
            <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-blue-600 mx-auto mb-4"></div>
            <p className="text-gray-500 text-lg">Loading contracts...</p>
          </div>
        ) : contractsError ? (
          <div className="text-center py-12">
            <AlertTriangle className="h-16 w-16 text-red-300 mx-auto mb-4" />
            <p className="text-red-500 text-lg">Failed to load contracts</p>
            <p className="text-gray-400">{contractsError}</p>
            <button 
              onClick={refetchContracts}
              className="btn-primary mt-4"
            >
              Try Again
            </button>
          </div>
        ) : !contractsData?.contracts || contractsData.contracts.length === 0 ? (
          <div className="text-center py-12">
            <FileText className="h-16 w-16 text-gray-300 mx-auto mb-4" />
            <p className="text-gray-500 text-lg">No contracts uploaded yet</p>
            <p className="text-gray-400">Upload your first contract to get started</p>
          </div>
        ) : (
          <div className="space-y-4">
            {contractsData.contracts.map((contract: any) => (
              <div key={contract.id} className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-3">
                    <FileText className="h-8 w-8 text-blue-600" />
                    <div>
                      <h3 className="font-medium">{contract.original_filename}</h3>
                      <p className="text-sm text-gray-500">
                        Uploaded {new Date(contract.upload_date).toLocaleDateString()} • 
                        {(contract.file_size / 1024).toFixed(1)} KB
                      </p>
                    </div>
                  </div>
                  <div className="flex items-center space-x-2">
                    <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                      contract.processed ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'
                    }`}>
                      {contract.processed ? 'Processed' : 'Pending'}
                    </span>
                    
                    {/* Analysis Button */}
                    <button 
                      onClick={() => handleAnalyze(contract.id)}
                      disabled={analyzing}
                      className="flex items-center space-x-1 px-3 py-1 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 text-sm font-medium"
                    >
                      <Brain className="h-4 w-4" />
                      <span>Analyze</span>
                    </button>
                    
                    {/* View Analysis Button */}
                    <button 
                      onClick={() => handleViewAnalysis(contract.id)}
                      className="flex items-center space-x-1 px-3 py-1 bg-green-600 text-white rounded-lg hover:bg-green-700 text-sm font-medium"
                    >
                      <BarChart3 className="h-4 w-4" />
                      <span>View Report</span>
                    </button>
                    
                    <button className="text-red-600 hover:text-red-700 text-sm font-medium">
                      <Trash2 className="h-4 w-4" />
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Quick Stats */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-8">
        <div className="card text-center">
          <div className="bg-red-100 w-12 h-12 rounded-full flex items-center justify-center mx-auto mb-3">
            <AlertTriangle className="h-6 w-6 text-red-600" />
          </div>
          <h3 className="text-2xl font-bold text-gray-900">3</h3>
          <p className="text-gray-600">High Risk Clauses</p>
        </div>

        <div className="card text-center">
          <div className="bg-green-100 w-12 h-12 rounded-full flex items-center justify-center mx-auto mb-3">
            <CheckCircle className="h-6 w-6 text-green-600" />
          </div>
          <h3 className="text-2xl font-bold text-gray-900">12</h3>
          <p className="text-gray-600">Contracts Analyzed</p>
        </div>

        <div className="card text-center">
          <div className="bg-blue-100 w-12 h-12 rounded-full flex items-center justify-center mx-auto mb-3">
            <Clock className="h-6 w-6 text-blue-600" />
          </div>
          <h3 className="text-2xl font-bold text-gray-900">2.3s</h3>
          <p className="text-gray-600">Avg Analysis Time</p>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
