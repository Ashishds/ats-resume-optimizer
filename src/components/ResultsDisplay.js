import React, { useState } from 'react';
import { Download, RotateCcw, FileText, CheckCircle, Star, AlertCircle, File } from 'lucide-react';
import { downloadFile } from '../services/api';

const ResultsDisplay = ({ results, onReset }) => {
  const [activeTab, setActiveTab] = useState(0);

  const tabs = [
    { id: 0, name: 'Cleaned Resume', icon: FileText },
    { id: 1, name: 'ATS Optimized', icon: CheckCircle },
    { id: 2, name: 'Final Resume', icon: Star },
    { id: 3, name: 'ATS Evaluation', icon: AlertCircle }
  ];

  const handleDownload = async (content, filename, format = 'txt') => {
    try {
      console.log(`Starting download: ${filename} (${format})`);
      await downloadFile(content, filename, format);
      console.log('Download completed successfully');
    } catch (error) {
      console.error('Download failed:', error);
      alert(`Download failed: ${error.message || 'Unknown error'}`);
    }
  };

  const renderEvaluation = (evaluation) => {
    // Try to parse evaluation if it's a string
    let parsedEvaluation = evaluation;
    if (typeof evaluation === 'string') {
      try {
        // Clean up the string to make it valid JSON
        let cleanString = evaluation.trim();
        
        // Remove markdown code blocks if present
        if (cleanString.includes('```json')) {
          cleanString = cleanString.replace(/```json\n?/, '').replace(/```\n?$/, '');
        }
        
        // Remove any leading/trailing whitespace
        cleanString = cleanString.trim();
        
        // Try to parse as JSON
        parsedEvaluation = JSON.parse(cleanString);
      } catch (error) {
        console.error('Failed to parse evaluation JSON:', error);
        // If parsing fails, show the raw text
        return (
          <div className="bg-gray-50 p-4 rounded-lg">
            <h4 className="font-semibold text-gray-900 mb-2">Raw Evaluation Output</h4>
            <pre className="whitespace-pre-wrap text-sm text-gray-700">
              {evaluation}
            </pre>
          </div>
        );
      }
    }

    if (typeof parsedEvaluation === 'object' && parsedEvaluation !== null) {
      return (
        <div className="space-y-6">
          {parsedEvaluation.overall_score && (
            <div className="bg-gradient-to-r from-primary-50 to-blue-50 p-6 rounded-lg">
              <div className="flex items-center justify-between">
                <h3 className="text-2xl font-bold text-gray-900">Overall ATS Score</h3>
                <div className="text-4xl font-bold text-primary-600">
                  {parsedEvaluation.overall_score}/100
                </div>
              </div>
            </div>
          )}

          {parsedEvaluation.breakdown && (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {Object.entries(parsedEvaluation.breakdown).map(([key, value]) => (
                <div key={key} className="bg-white p-4 rounded-lg border border-gray-200">
                  <h4 className="font-semibold text-gray-900 capitalize">
                    {key.replace(/_/g, ' ')}
                  </h4>
                  <div className="text-2xl font-bold text-primary-600 mt-2">
                    {value}/5
                  </div>
                </div>
              ))}
            </div>
          )}

          {parsedEvaluation.missing_keywords && parsedEvaluation.missing_keywords.length > 0 && (
            <div className="bg-yellow-50 p-4 rounded-lg border border-yellow-200">
              <h4 className="font-semibold text-yellow-800 mb-2">Missing Keywords</h4>
              <div className="flex flex-wrap gap-2">
                {parsedEvaluation.missing_keywords.map((keyword, index) => (
                  <span
                    key={index}
                    className="px-3 py-1 bg-yellow-100 text-yellow-800 rounded-full text-sm"
                  >
                    {keyword}
                  </span>
                ))}
              </div>
            </div>
          )}

          {parsedEvaluation.quick_wins && parsedEvaluation.quick_wins.length > 0 && (
            <div className="bg-green-50 p-4 rounded-lg border border-green-200">
              <h4 className="font-semibold text-green-800 mb-2">Quick Wins</h4>
              <ul className="list-disc list-inside space-y-1">
                {parsedEvaluation.quick_wins.map((win, index) => (
                  <li key={index} className="text-green-700">{win}</li>
                ))}
              </ul>
            </div>
          )}

          {parsedEvaluation.summary && (
            <div className="bg-gray-50 p-4 rounded-lg">
              <h4 className="font-semibold text-gray-900 mb-2">Summary</h4>
              <p className="text-gray-700">{parsedEvaluation.summary}</p>
            </div>
          )}
        </div>
      );
    }

    return (
      <div className="bg-gray-50 p-4 rounded-lg">
        <h4 className="font-semibold text-gray-900 mb-2">Raw Evaluation Output</h4>
        <pre className="whitespace-pre-wrap text-sm text-gray-700">
          {JSON.stringify(evaluation, null, 2)}
        </pre>
      </div>
    );
  };

  return (
    <div className="bg-white rounded-lg shadow-lg">
      {/* Header */}
      <div className="flex items-center justify-between p-6 border-b border-gray-200">
        <h2 className="text-2xl font-bold text-gray-900">Processing Results</h2>
        <button
          onClick={onReset}
          className="flex items-center gap-2 px-4 py-2 text-gray-600 hover:text-gray-800 transition-colors duration-200"
        >
          <RotateCcw className="h-4 w-4" />
          Process Another Resume
        </button>
      </div>

      {/* Tabs */}
      <div className="border-b border-gray-200">
        <nav className="flex space-x-8 px-6">
          {tabs.map((tab) => {
            const Icon = tab.icon;
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`flex items-center gap-2 py-4 px-1 border-b-2 font-medium text-sm transition-colors duration-200 ${
                  activeTab === tab.id
                    ? 'border-primary-500 text-primary-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                <Icon className="h-4 w-4" />
                {tab.name}
              </button>
            );
          })}
        </nav>
      </div>

      {/* Tab Content */}
      <div className="p-6">
        {activeTab === 0 && (
          <div>
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-xl font-semibold text-gray-900">Cleaned Resume</h3>
              <button
                onClick={() => handleDownload(results.cleaned, 'cleaned_resume.pdf', 'pdf')}
                className="flex items-center gap-2 px-6 py-3 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors duration-200 font-medium"
              >
                <File className="h-5 w-5" />
                Download PDF
              </button>
            </div>
            <div className="bg-gray-50 p-4 rounded-lg">
              <pre className="whitespace-pre-wrap text-sm text-gray-700">
                {results.cleaned}
              </pre>
            </div>
          </div>
        )}

        {activeTab === 1 && (
          <div>
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-xl font-semibold text-gray-900">ATS Optimized Resume</h3>
              <button
                onClick={() => handleDownload(results.rewritten, 'rewritten_resume.pdf', 'pdf')}
                className="flex items-center gap-2 px-6 py-3 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors duration-200 font-medium"
              >
                <File className="h-5 w-5" />
                Download PDF
              </button>
            </div>
            <div className="bg-gray-50 p-4 rounded-lg">
              <pre className="whitespace-pre-wrap text-sm text-gray-700">
                {results.rewritten}
              </pre>
            </div>
          </div>
        )}

        {activeTab === 2 && (
          <div>
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-xl font-semibold text-gray-900">Final Resume</h3>
              <div className="flex gap-2">
                <button
                  onClick={() => handleDownload(results.final, 'final_resume.docx', 'docx')}
                  className="flex items-center gap-2 px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors duration-200 font-medium"
                >
                  <FileText className="h-5 w-5" />
                  Download DOCX
                </button>
                <button
                  onClick={() => handleDownload(results.final, 'final_resume.pdf', 'pdf')}
                  className="flex items-center gap-2 px-6 py-3 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors duration-200 font-medium"
                >
                  <File className="h-5 w-5" />
                  Download PDF
                </button>
              </div>
            </div>
            <div className="bg-gray-50 p-4 rounded-lg">
              <pre className="whitespace-pre-wrap text-sm text-gray-700">
                {results.final}
              </pre>
            </div>
          </div>
        )}

        {activeTab === 3 && (
          <div>
            <h3 className="text-xl font-semibold text-gray-900 mb-4">ATS Evaluation & Suggestions</h3>
            {renderEvaluation(results.evaluation)}
          </div>
        )}
      </div>
    </div>
  );
};

export default ResultsDisplay;
