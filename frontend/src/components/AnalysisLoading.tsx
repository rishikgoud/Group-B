import React from 'react';

interface AnalysisLoadingProps {
  isVisible: boolean;
  message?: string;
}

const AnalysisLoading: React.FC<AnalysisLoadingProps> = ({ 
  isVisible, 
  message = "Analyzing contract with AI..." 
}) => {
  if (!isVisible) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50 backdrop-blur-sm">
      <div className="bg-white rounded-2xl p-8 shadow-2xl max-w-md w-full mx-4">
        {/* Spinning Circle Animation */}
        <div className="flex flex-col items-center space-y-6">
          <div className="relative">
            {/* Outer rotating ring */}
            <div className="w-20 h-20 border-4 border-blue-200 rounded-full animate-spin border-t-blue-600"></div>
            {/* Inner pulsing dot */}
            <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2">
              <div className="w-3 h-3 bg-blue-600 rounded-full animate-pulse"></div>
            </div>
          </div>
          
          {/* Loading text */}
          <div className="text-center">
            <h3 className="text-xl font-semibold text-gray-800 mb-2">
              AI Analysis in Progress
            </h3>
            <p className="text-gray-600 mb-4">{message}</p>
            
            {/* Progress dots */}
            <div className="flex space-x-1 justify-center">
              <div className="w-2 h-2 bg-blue-600 rounded-full animate-bounce"></div>
              <div className="w-2 h-2 bg-blue-600 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
              <div className="w-2 h-2 bg-blue-600 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
            </div>
          </div>
          
          {/* Analysis steps */}
          <div className="w-full space-y-2">
            <div className="flex items-center text-sm text-gray-600">
              <div className="w-2 h-2 bg-green-500 rounded-full mr-3 animate-pulse"></div>
              <span>Extracting text from document</span>
            </div>
            <div className="flex items-center text-sm text-gray-600">
              <div className="w-2 h-2 bg-yellow-500 rounded-full mr-3 animate-pulse"></div>
              <span>Identifying contract clauses</span>
            </div>
            <div className="flex items-center text-sm text-gray-600">
              <div className="w-2 h-2 bg-blue-500 rounded-full mr-3 animate-pulse"></div>
              <span>Assessing risk levels</span>
            </div>
            <div className="flex items-center text-sm text-gray-600">
              <div className="w-2 h-2 bg-purple-500 rounded-full mr-3 animate-pulse"></div>
              <span>Generating insights</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AnalysisLoading;
