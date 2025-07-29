import { useState, useEffect } from 'react';
import { apiService } from '../services/api.js';
import { apiConfig } from '../config/api.js';

function ApiStatus() {
  const [status, setStatus] = useState('checking');
  const [lastChecked, setLastChecked] = useState(null);
  const [responseTime, setResponseTime] = useState(null);
  const [error, setError] = useState(null);

  const checkApiStatus = async () => {
    setStatus('checking');
    setError(null);
    const startTime = Date.now();

    try {
      const healthStatus = await apiService.getHealthStatus();
      setStatus('healthy');
      setResponseTime(healthStatus.responseTime);
      setLastChecked(new Date().toLocaleTimeString());
    } catch (err) {
      setStatus('unhealthy');
      setError(err.message);
      setLastChecked(new Date().toLocaleTimeString());
    }
  };

  useEffect(() => {
    checkApiStatus();
  }, []);

  // Debug information
  const debugInfo = {
    apiUrl: apiConfig.apiUrl,
    environment: import.meta.env.MODE,
    viteApiUrl: import.meta.env.VITE_API_URL,
    dev: import.meta.env.DEV,
    prod: import.meta.env.PROD,
  };

  return (
    <div className="card">
      <div className="card-header">
        <h3 className="card-title">API Status</h3>
      </div>
      <div className="card-content">
        <div className="flex items-center space-x-2 mb-4">
          <div className={`w-3 h-3 rounded-full ${
            status === 'healthy' ? 'bg-green-500' : 
            status === 'unhealthy' ? 'bg-red-500' : 'bg-yellow-500'
          }`}></div>
          <span className="text-sm font-medium">
            {status === 'healthy' ? 'API is running' : 
             status === 'unhealthy' ? 'API is down' : 'Checking...'}
          </span>
        </div>

        {status === 'healthy' && (
          <div className="space-y-2 text-sm text-gray-600">
            <p>API Server is running ✅</p>
            {responseTime && <p>Response time: {responseTime}ms</p>}
            {lastChecked && <p>Last checked: {lastChecked}</p>}
          </div>
        )}

        {status === 'unhealthy' && (
          <div className="space-y-2 text-sm text-red-600">
            <p>❌ {error}</p>
            {lastChecked && <p>Last checked: {lastChecked}</p>}
          </div>
        )}

        {/* Debug Information */}
        <details className="mt-4">
          <summary className="cursor-pointer text-sm text-gray-500 hover:text-gray-700">
            Debug Information
          </summary>
          <div className="mt-2 p-2 bg-gray-100 rounded text-xs">
            <pre className="whitespace-pre-wrap">
              {JSON.stringify(debugInfo, null, 2)}
            </pre>
          </div>
        </details>

        <button
          onClick={checkApiStatus}
          disabled={status === 'checking'}
          className="mt-4 w-full btn btn-primary btn-sm"
        >
          {status === 'checking' ? 'Checking...' : 'Check Again'}
        </button>
      </div>
    </div>
  );
}

export default ApiStatus; 