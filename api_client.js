/**
 * Ultimate Guitar Tab Parser API Client
 * 
 * This module provides functions to interact with the Flask API
 * for parsing Ultimate Guitar tabs.
 */

class UltimateGuitarApiClient {
    constructor(baseUrl = 'http://127.0.0.1:5000') {
        this.baseUrl = baseUrl;
    }

    /**
     * Test if the API server is running
     * @returns {Promise<string>} The response from the server
     */
    async testConnection() {
        try {
            const response = await fetch(`${this.baseUrl}/`);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return await response.text();
        } catch (error) {
            throw new Error(`Failed to connect to API: ${error.message}`);
        }
    }

    /**
     * Parse an Ultimate Guitar tab URL
     * @param {string} url - The Ultimate Guitar tab URL
     * @returns {Promise<Object>} The parsed tab data
     */
    async parseTab(url) {
        if (!url) {
            throw new Error('URL is required');
        }

        try {
            const response = await fetch(`${this.baseUrl}/tab?url=${encodeURIComponent(url)}`);
            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || 'Failed to parse tab');
            }

            return data;
        } catch (error) {
            throw new Error(`Failed to parse tab: ${error.message}`);
        }
    }

    /**
     * Get tab information for multiple URLs
     * @param {string[]} urls - Array of Ultimate Guitar tab URLs
     * @returns {Promise<Object[]>} Array of parsed tab data
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
                    data: result
                });
            } catch (error) {
                errors.push({
                    index: i,
                    url: urls[i],
                    success: false,
                    error: error.message
                });
            }
        }

        return {
            results,
            errors,
            total: urls.length,
            successful: results.length,
            failed: errors.length
        };
    }
}

// Export for different module systems
if (typeof module !== 'undefined' && module.exports) {
    // Node.js
    module.exports = UltimateGuitarApiClient;
} else if (typeof define === 'function' && define.amd) {
    // AMD
    define([], function() {
        return UltimateGuitarApiClient;
    });
} else {
    // Browser global
    window.UltimateGuitarApiClient = UltimateGuitarApiClient;
}

// Example usage:
/*
// Browser usage:
const apiClient = new UltimateGuitarApiClient();

// Test connection
apiClient.testConnection()
    .then(response => console.log('API is running:', response))
    .catch(error => console.error('API error:', error));

// Parse a tab
apiClient.parseTab('https://tabs.ultimate-guitar.com/tab/artist/song-name-123456')
    .then(tabData => console.log('Parsed tab:', tabData))
    .catch(error => console.error('Parse error:', error));

// Parse multiple tabs
const urls = [
    'https://tabs.ultimate-guitar.com/tab/artist1/song1-123456',
    'https://tabs.ultimate-guitar.com/tab/artist2/song2-789012'
];

apiClient.parseMultipleTabs(urls)
    .then(results => {
        console.log('Successful:', results.successful);
        console.log('Failed:', results.failed);
        console.log('Results:', results.results);
        console.log('Errors:', results.errors);
    })
    .catch(error => console.error('Batch parse error:', error));
*/ 