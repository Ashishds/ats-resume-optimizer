import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 300000, // 5 minutes timeout for AI processing
});

export const processResume = async (file, jobTitle, jobDescription) => {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('job_title', jobTitle);
  formData.append('job_description', jobDescription);

  const response = await api.post('/process-resume', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });

  return response;
};

export const downloadFile = async (content, filename, format = 'txt') => {
  try {
    console.log(`API: Preparing download for ${filename} (${format})`);
    console.log(`API: Base URL: ${API_BASE_URL}`);
    
    const formData = new FormData();
    formData.append('content', content);
    formData.append('filename', filename);

    let endpoint;
    switch (format) {
      case 'docx':
        endpoint = '/download-docx';
        break;
      case 'pdf':
        endpoint = '/download-pdf';
        break;
      default:
        endpoint = '/download-txt';
    }
    
    const fullUrl = `${API_BASE_URL}${endpoint}`;
    console.log(`API: Full URL: ${fullUrl}`);
    console.log(`API: Content length: ${content.length} characters`);
    
    const response = await api.post(endpoint, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
      responseType: 'blob',
    });

    console.log(`API: Response received, size: ${response.data.size} bytes`);
    console.log(`API: Response status: ${response.status}`);

    // Create blob link to download
    const url = window.URL.createObjectURL(new Blob([response.data]));
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', filename);
    document.body.appendChild(link);
    link.click();
    link.remove();
    window.URL.revokeObjectURL(url);
    
    console.log(`API: Download initiated for ${filename}`);
  } catch (error) {
    console.error('API: Download error:', error);
    console.error('API: Error response:', error.response);
    console.error('API: Error status:', error.response?.status);
    console.error('API: Error data:', error.response?.data);
    throw new Error(`Download failed: ${error.response?.data?.detail || error.message}`);
  }
};

export default api;
