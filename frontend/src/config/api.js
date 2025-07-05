/**
 * API Configuration
 * Handles different environments (development, staging, production)
 */

const config = {
  development: {
    apiUrl: 'http://127.0.0.1:5000',
    timeout: 10000,
  },
  staging: {
    apiUrl: process.env.VITE_API_URL || 'https://staging-api.yourdomain.com',
    timeout: 15000,
  },
  production: {
    apiUrl: process.env.VITE_API_URL || 'http://127.0.0.1:5000',
    timeout: 40000,
  },
};

// Get current environment
const environment = import.meta.env.MODE || 'development';

// Export the appropriate configuration
export const apiConfig = config[environment];

// API endpoints
export const endpoints = {
  status: '/',
  parseTab: '/tab',
};

// Helper function to get full API URL
export const getApiUrl = (endpoint) => {
  return `${apiConfig.apiUrl}${endpoint}`;
};

// Log configuration in development
if (environment === 'development') {
  console.log(`🚀 API Config:`, {
    environment,
    apiUrl: apiConfig.apiUrl,
    timeout: apiConfig.timeout,
  });
} 