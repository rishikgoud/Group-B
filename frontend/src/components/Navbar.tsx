import React from 'react';
import { Link } from 'react-router-dom';
import { Scale, Upload, MessageCircle, BarChart3, Database } from 'lucide-react';

const Navbar: React.FC = () => {
  return (
    <nav className="bg-white shadow-sm border-b border-gray-200">
      <div className="container mx-auto px-4">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <Link to="/" className="flex items-center space-x-2">
            <Scale className="h-8 w-8 text-blue-600" />
            <span className="text-xl font-bold text-gray-900">LegalEase AI</span>
          </Link>

          {/* Navigation Links */}
          <div className="hidden md:flex items-center space-x-8">
            <Link 
              to="/dashboard" 
              className="text-gray-600 hover:text-blue-600 transition-colors duration-200 flex items-center space-x-1"
            >
              <Upload className="h-4 w-4" />
              <span>Upload</span>
            </Link>
            <Link 
              to="/chat" 
              className="text-gray-600 hover:text-blue-600 transition-colors duration-200 flex items-center space-x-1"
            >
              <MessageCircle className="h-4 w-4" />
              <span>Ask LegalEase</span>
            </Link>
            <Link 
              to="/analytics" 
              className="text-gray-600 hover:text-blue-600 transition-colors duration-200 flex items-center space-x-1"
            >
              <BarChart3 className="h-4 w-4" />
              <span>Analytics</span>
            </Link>
            <Link 
              to="/dataset" 
              className="text-gray-600 hover:text-blue-600 transition-colors duration-200 flex items-center space-x-1"
            >
              <Database className="h-4 w-4" />
              <span>Dataset</span>
            </Link>
          </div>

          {/* Mobile menu button */}
          <div className="md:hidden">
            <button className="text-gray-600 hover:text-blue-600">
              <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
              </svg>
            </button>
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
