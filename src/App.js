import React, { useState } from 'react';
import FileUpload from './components/FileUpload';
import JobForm from './components/JobForm';
import ResultsDisplay from './components/ResultsDisplay';
import LoadingSpinner from './components/LoadingSpinner';
import { processResume } from './services/api';

function App() {
  const [file, setFile] = useState(null);
  const [jobTitle, setJobTitle] = useState('');
  const [jobDescription, setJobDescription] = useState('');
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [loadingStep, setLoadingStep] = useState('');
  const [error, setError] = useState(null);

  const handleSubmit = async () => {
    if (!file) {
      setError('Please upload a resume file.');
      return;
    }
    if (!jobTitle.trim() || !jobDescription.trim()) {
      setError('Please provide both job title and job description.');
      return;
    }

    setLoading(true);
    setError(null);
    setLoadingStep('Initializing AI agents...');

    try {
      const steps = [
        'Initializing AI agents...',
        'Stage 1/4: Parsing and cleaning resume...',
        'Stage 2/4: ATS optimization...',
        'Stage 3/4: Bullet point refinement...',
        'Stage 4/4: Final ATS evaluation...',
        'Complete!'
      ];
      
      let currentStep = 0;
      const stepInterval = setInterval(() => {
        if (currentStep < steps.length - 1) {
          setLoadingStep(steps[currentStep]);
          currentStep++;
        } else {
          clearInterval(stepInterval);
        }
      }, 15000); // Update every 15 seconds
      
      setLoadingStep(steps[0]);
      const response = await processResume(file, jobTitle, jobDescription);
      clearInterval(stepInterval);
      setResults(response.data.results);
      setLoadingStep('Complete!');
    } catch (err) {
      setError(err.response?.data?.detail || 'An error occurred while processing your resume.');
    } finally {
      setLoading(false);
      setLoadingStep('');
    }
  };

  const handleReset = () => {
    setFile(null);
    setJobTitle('');
    setJobDescription('');
    setResults(null);
    setError(null);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            🧠 Intelligent Resume Optimization System
          </h1>
          <p className="text-lg text-gray-600 max-w-3xl mx-auto">
            Upload your resume, target a role, and get an ATS-friendly version with scores & quick wins using AI agents.
          </p>
        </div>

        {/* Main Content */}
        <div className="max-w-6xl mx-auto">
          {!results ? (
            <div className="bg-white rounded-lg shadow-lg p-8">
              {/* File Upload */}
              <div className="mb-8">
                <h2 className="text-2xl font-semibold text-gray-900 mb-4">Upload Resume</h2>
                <FileUpload file={file} onFileChange={setFile} />
              </div>

              {/* Job Information */}
              <div className="mb-8">
                <h2 className="text-2xl font-semibold text-gray-900 mb-4">Target Job Information</h2>
                <JobForm
                  jobTitle={jobTitle}
                  jobDescription={jobDescription}
                  onJobTitleChange={setJobTitle}
                  onJobDescriptionChange={setJobDescription}
                />
              </div>

              {/* Error Display */}
              {error && (
                <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg">
                  <p className="text-red-800">{error}</p>
                </div>
              )}

              {/* Submit Button */}
              <div className="flex justify-center">
                <button
                  onClick={handleSubmit}
                  disabled={loading}
                  className="bg-primary-600 hover:bg-primary-700 disabled:bg-gray-400 text-white font-semibold py-3 px-8 rounded-lg transition-colors duration-200 flex items-center gap-2"
                >
                  {loading ? (
                    <>
                      <LoadingSpinner size="sm" />
                      {loadingStep || 'Processing Resume...'}
                    </>
                  ) : (
                    '🚀 Run ATS Agent'
                  )}
                </button>
              </div>
            </div>
          ) : (
            <ResultsDisplay results={results} onReset={handleReset} />
          )}
        </div>
      </div>
    </div>
  );
}

export default App;
