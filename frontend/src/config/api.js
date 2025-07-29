/**
 * API Configuration
 * Handles different environments (development, staging, production)
 */

// Get the API URL from environment variable
const apiUrl = import.meta.env.VITE_API_URL;

// Log the environment variable for debugging
console.log('🔍 Environment Variable Check:', {
  VITE_API_URL: import.meta.env.VITE_API_URL,
  MODE: import.meta.env.MODE,
  DEV: import.meta.env.DEV,
  PROD: import.meta.env.PROD,
});

const config = {
  development: {
    apiUrl: apiUrl || 'http://localhost:5000',
    timeout: 120000, // Increased to 120 seconds for development
  },
  staging: {
    apiUrl: apiUrl || 'https://ultimate-api-production.up.railway.app',
    timeout: 120000, // Increased to 120 seconds for staging
  },
  production: {
    apiUrl: apiUrl || 'https://ultimate-api-production.up.railway.app',
    timeout: 120000, // Increased to 120 seconds for production
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