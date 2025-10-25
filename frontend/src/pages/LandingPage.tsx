import React from 'react';
import { Link } from 'react-router-dom';
import { Upload, FileText, MessageCircle, BarChart3, ArrowRight, Shield, Zap, Brain, Database } from 'lucide-react';

const LandingPage: React.FC = () => {
  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="gradient-bg legal-pattern text-white py-20">
        <div className="container mx-auto px-4 text-center">
          <h1 className="text-5xl md:text-6xl font-bold mb-6 animate-fade-in">
            ⚖️ LegalEase AI
          </h1>
          <p className="text-xl md:text-2xl mb-8 text-blue-100 max-w-3xl mx-auto">
            Understand. Analyze. Protect.
          </p>
          <p className="text-lg mb-12 text-blue-200 max-w-4xl mx-auto">
            Empowering individuals and businesses to decode complex contracts using AI. 
            Upload your contracts, get instant analysis, and understand every clause in plain English.
          </p>
          
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link 
              to="/dashboard" 
              className="bg-white text-blue-600 hover:bg-blue-50 font-semibold py-3 px-8 rounded-lg transition-colors duration-200 flex items-center justify-center space-x-2"
            >
              <Upload className="h-5 w-5" />
              <span>Upload Contract</span>
              <ArrowRight className="h-4 w-4" />
            </Link>
            <Link 
              to="/chat" 
              className="border-2 border-white text-white hover:bg-white hover:text-blue-600 font-semibold py-3 px-8 rounded-lg transition-colors duration-200 flex items-center justify-center space-x-2"
            >
              <MessageCircle className="h-5 w-5" />
              <span>Try AI Chat</span>
            </Link>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 bg-white">
        <div className="container mx-auto px-4">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">
              How LegalEase AI Works
            </h2>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              Our AI-powered platform makes contract analysis simple, fast, and accessible to everyone.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {/* Upload */}
            <div className="card text-center animate-slide-up">
              <div className="bg-blue-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-6">
                <Upload className="h-8 w-8 text-blue-600" />
              </div>
              <h3 className="text-xl font-semibold mb-4">1. Upload Contract</h3>
              <p className="text-gray-600">
                Upload any contract in PDF, DOCX, or image format. Our AI extracts and processes the text automatically.
              </p>
            </div>

            {/* Analyze */}
            <div className="card text-center animate-slide-up">
              <div className="bg-green-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-6">
                <Brain className="h-8 w-8 text-green-600" />
              </div>
              <h3 className="text-xl font-semibold mb-4">2. AI Analysis</h3>
              <p className="text-gray-600">
                Our AI identifies clauses, assesses risks, and provides plain English explanations of complex legal terms.
              </p>
            </div>

            {/* Understand */}
            <div className="card text-center animate-slide-up">
              <div className="bg-purple-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-6">
                <Shield className="h-8 w-8 text-purple-600" />
              </div>
              <h3 className="text-xl font-semibold mb-4">3. Understand & Protect</h3>
              <p className="text-gray-600">
                Get actionable insights, risk assessments, and recommendations to make informed decisions about your contracts.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Key Features */}
      <section className="py-20 bg-gray-50">
        <div className="container mx-auto px-4">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">
              Key Features
            </h2>
            <p className="text-xl text-gray-600">
              Everything you need to understand and analyze contracts
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            <div className="card hover:shadow-lg transition-shadow duration-200">
              <FileText className="h-8 w-8 text-blue-600 mb-4" />
              <h3 className="text-lg font-semibold mb-2">Clause Extraction</h3>
              <p className="text-gray-600 text-sm">
                Automatically identify and categorize contract clauses by type and importance.
              </p>
            </div>

            <div className="card hover:shadow-lg transition-shadow duration-200">
              <Zap className="h-8 w-8 text-yellow-600 mb-4" />
              <h3 className="text-lg font-semibold mb-2">Risk Assessment</h3>
              <p className="text-gray-600 text-sm">
                Get color-coded risk levels for each clause with detailed explanations.
              </p>
            </div>

            <div className="card hover:shadow-lg transition-shadow duration-200">
              <MessageCircle className="h-8 w-8 text-green-600 mb-4" />
              <h3 className="text-lg font-semibold mb-2">AI Chat Assistant</h3>
              <p className="text-gray-600 text-sm">
                Ask questions about your contract and get instant, contextual answers.
              </p>
            </div>

            <div className="card hover:shadow-lg transition-shadow duration-200">
              <BarChart3 className="h-8 w-8 text-purple-600 mb-4" />
              <h3 className="text-lg font-semibold mb-2">Analytics Dashboard</h3>
              <p className="text-gray-600 text-sm">
                Visualize contract insights with interactive charts and risk distributions.
              </p>
            </div>

            <div className="card hover:shadow-lg transition-shadow duration-200">
              <Database className="h-8 w-8 text-indigo-600 mb-4" />
              <h3 className="text-lg font-semibold mb-2">Dataset Explorer</h3>
              <p className="text-gray-600 text-sm">
                Explore real legal clauses from our comprehensive dataset for learning and comparison.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-blue-600 text-white">
        <div className="container mx-auto px-4 text-center">
          <h2 className="text-4xl font-bold mb-6">
            Ready to Analyze Your Contracts?
          </h2>
          <p className="text-xl mb-8 text-blue-100">
            Join thousands of users who trust LegalEase AI for their contract analysis needs.
          </p>
          <Link 
            to="/dashboard" 
            className="bg-white text-blue-600 hover:bg-blue-50 font-semibold py-3 px-8 rounded-lg transition-colors duration-200 inline-flex items-center space-x-2"
          >
            <span>Get Started Now</span>
            <ArrowRight className="h-5 w-5" />
          </Link>
        </div>
      </section>
    </div>
  );
};

export default LandingPage;
