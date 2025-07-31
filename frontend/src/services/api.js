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

// Log the actual timeout being used
console.log(`🔧 Axios timeout configured: ${apiConfig.timeout}ms`);
console.log(`🔧 Axios instance timeout: ${apiClient.defaults.timeout}ms`);

// Override any default timeouts
apiClient.defaults.timeout = apiConfig.timeout;

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
      timeout: error.config?.timeout,
      code: error.code,
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
      const response = await apiClient.get('/api/health');
      return response.data;
    } catch (error) {
      throw new Error(`❌ Failed to connect to API: ${error.response?.data?.error || error.message}`);
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

    console.log(`🎯 Starting tab parse for: ${url}`);
    const startTime = Date.now();

    try {
      const response = await apiClient.get('/tab', {
        params: { url },
        timeout: apiConfig.timeout, // Explicitly set timeout for this request
      });
      
      const responseTime = Date.now() - startTime;
      console.log(`✅ Tab parse completed in ${responseTime}ms`);
      console.log(`📦 Response data:`, response.data);
      
      return response.data;
    } catch (error) {
      const responseTime = Date.now() - startTime;
      console.error(`❌ Tab parse failed after ${responseTime}ms:`, error);
      
      if (error.code === 'ECONNABORTED') {
        throw new Error(`Request timed out after ${responseTime}ms. The server took too long to respond.`);
      }
      
      if (error.response?.status === 500) {
        throw new Error(error.response.data.error || 'Failed to parse tab');
      }
      
      throw new Error(`Request failed: ${error.response?.data?.error || error.message}`);
    }
  }

  /**
   * Search for a song by name and get the Ultimate Guitar URL
   * @param {string} songName - Name of the song to search for
   * @param {string} artistName - Optional artist name to improve search accuracy
   * @returns {Promise<Object>} Search result with URL
   */
  async searchSong(songName, artistName = '') {
    if (!songName) {
      throw new Error('Song name is required');
    }

    console.log(`🎯 Starting song search for: "${songName}"${artistName ? ` by ${artistName}` : ''}`);
    const startTime = Date.now();

    try {
      const params = { song: songName };
      if (artistName) {
        params.artist = artistName;
      }

      const response = await apiClient.get('/search', {
        params,
        timeout: apiConfig.timeout,
      });
      
      const responseTime = Date.now() - startTime;
      console.log(`✅ Song search completed in ${responseTime}ms`);
      console.log(`📦 Response data:`, response.data);
      
      return response.data;
    } catch (error) {
      const responseTime = Date.now() - startTime;
      console.error(`❌ Song search failed after ${responseTime}ms:`, error);
      
      if (error.code === 'ECONNABORTED') {
        throw new Error(`Request timed out after ${responseTime}ms. The server took too long to respond.`);
      }
      
      if (error.response?.status === 404) {
        throw new Error(error.response.data.error || 'No tabs found for this song');
      }
      
      if (error.response?.status === 500) {
        throw new Error(error.response.data.error || 'Failed to search for song');
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
   * Parse Ultimate Guitar tab in combined format
   * @param {string} url - Ultimate Guitar tab URL
   * @returns {Promise<Object>} Combined tab data with chords and lyrics aligned
   */
  async parseCombinedTab(url) {
    if (!url) {
      throw new Error('URL is required');
    }

    console.log(`🎯 Starting combined tab parse for: ${url}`);
    const startTime = Date.now();

    try {
      const response = await apiClient.get('/tab/combined', {
        params: { url },
        timeout: apiConfig.timeout,
      });
      
      const responseTime = Date.now() - startTime;
      console.log(`✅ Combined tab parse completed in ${responseTime}ms`);
      
      return response.data;
    } catch (error) {
      const responseTime = Date.now() - startTime;
      console.error(`❌ Combined tab parse failed after ${responseTime}ms:`, error);
      
      if (error.response?.status === 400) {
        throw new Error(`Invalid request: ${error.response.data.error || 'Bad request'}`);
      } else if (error.response?.status === 404) {
        throw new Error(`Tab not found: ${error.response.data.error || 'URL not found'}`);
      } else if (error.response?.status >= 500) {
        throw new Error(`Server error: ${error.response.data.error || 'Internal server error'}`);
      } else if (error.code === 'ECONNABORTED' || error.message.includes('timeout')) {
        throw new Error(`Request timed out after ${apiConfig.timeout}ms. The server may be busy or the URL may be invalid.`);
      } else {
        throw new Error(`Failed to parse combined tab: ${error.response?.data?.error || error.message}`);
      }
    }
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

      // Health Check Message
      let message = 'API Server is running ✅';

      return {
        status: 'healthy',
        message,
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