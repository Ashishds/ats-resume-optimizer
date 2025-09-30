import React from 'react';

const JobForm = ({ jobTitle, jobDescription, onJobTitleChange, onJobDescriptionChange }) => {
  return (
    <div className="space-y-6">
      <div>
        <label htmlFor="job-title" className="block text-sm font-medium text-gray-700 mb-2">
          Target Job Title
        </label>
        <input
          type="text"
          id="job-title"
          value={jobTitle}
          onChange={(e) => onJobTitleChange(e.target.value)}
          placeholder="e.g., Machine Learning Engineer, Software Developer, Data Scientist"
          className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors duration-200"
        />
      </div>
      
      <div>
        <label htmlFor="job-description" className="block text-sm font-medium text-gray-700 mb-2">
          Job Description
        </label>
        <textarea
          id="job-description"
          value={jobDescription}
          onChange={(e) => onJobDescriptionChange(e.target.value)}
          placeholder="Paste the job description here..."
          rows={8}
          className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors duration-200 resize-vertical"
        />
        <p className="text-sm text-gray-500 mt-2">
          Include key requirements, skills, and responsibilities for better optimization
        </p>
      </div>
    </div>
  );
};

export default JobForm;
