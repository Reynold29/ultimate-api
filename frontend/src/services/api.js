import axios from 'axios';
import { apiConfig, getApiUrl } from '../config/api.js';

/**
 * API Service
 * Handles all API communication with proper error handling and interceptors
 */

// Create axios instance with default configuration
const apiClient = axios.create({
  baseURL: apiConfig.apiUrl,
  timeout: apiConfig.timeout,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor
apiClient.interceptors.request.use(
  (config) => {
    // Add loading state or auth headers here if needed
    console.log(`🌐 API Request: ${config.method?.toUpperCase()} ${config.url}`);
    return config;
  },
  (error) => {
    console.error('❌ Request Error:', error);
    return Promise.reject(error);
  }
);

// Response interceptor
apiClient.interceptors.response.use(
  (response) => {
    console.log(`✅ API Response: ${response.status} ${response.config.url}`);
    return response;
  },
  (error) => {
    console.error('❌ Response Error:', {
      status: error.response?.status,
      message: error.response?.data?.error || error.message,
      url: error.config?.url,
    });
    return Promise.reject(error);
  }
);

/**
 * API Service Class
 */
class ApiService {
  /**
   * Test API connection
   * @returns {Promise<string>} Server status message
   */
  async testConnection() {
    try {
      const response = await apiClient.get('/');
      return response.data;
    } catch (error) {
      throw new Error(`Failed to connect to API: ${error.response?.data?.error || error.message}`);
    }
  }

  /**
   * Parse Ultimate Guitar tab
   * @param {string} url - Ultimate Guitar tab URL
   * @returns {Promise<Object>} Parsed tab data
   */
  async parseTab(url) {
    if (!url) {
      throw new Error('URL is required');
    }

    try {
      const response = await apiClient.get('/tab', {
        params: { url },
      });
      return response.data;
    } catch (error) {
      if (error.response?.status === 500) {
        throw new Error(error.response.data.error || 'Failed to parse tab');
      }
      throw new Error(`Request failed: ${error.response?.data?.error || error.message}`);
    }
  }

  /**
   * Parse multiple tabs
   * @param {string[]} urls - Array of Ultimate Guitar tab URLs
   * @returns {Promise<Object>} Results with success/error tracking
   */
  async parseMultipleTabs(urls) {
    if (!Array.isArray(urls) || urls.length === 0) {
      throw new Error('URLs array is required and must not be empty');
    }

    const results = [];
    const errors = [];

    for (let i = 0; i < urls.length; i++) {
      try {
        const result = await this.parseTab(urls[i]);
        results.push({
          index: i,
          url: urls[i],
          success: true,
          data: result,
        });
      } catch (error) {
        errors.push({
          index: i,
          url: urls[i],
          success: false,
          error: error.message,
        });
      }
    }

    return {
      results,
      errors,
      total: urls.length,
      successful: results.length,
      failed: errors.length,
    };
  }

  /**
   * Get API health status
   * @returns {Promise<Object>} Health status information
   */
  async getHealthStatus() {
    try {
      const startTime = Date.now();
      const response = await this.testConnection();
      const responseTime = Date.now() - startTime;

      return {
        status: 'healthy',
        message: response,
        responseTime,
        timestamp: new Date().toISOString(),
      };
    } catch (error) {
      return {
        status: 'unhealthy',
        error: error.message,
        timestamp: new Date().toISOString(),
      };
    }
  }
}

// Export singleton instance
export const apiService = new ApiService();

// Export for testing or direct usage
export default ApiService; 