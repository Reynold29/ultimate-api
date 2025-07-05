import { useState, useEffect } from 'react';
import { Wifi, WifiOff, Clock, CheckCircle, XCircle } from 'lucide-react';
import { apiService } from '../services/api.js';

const ApiStatus = () => {
  const [status, setStatus] = useState('idle'); // 'idle', 'loading', 'healthy', 'unhealthy'
  const [healthData, setHealthData] = useState(null);
  const [lastChecked, setLastChecked] = useState(null);

  const checkHealth = async () => {
    setStatus('loading');
    try {
      const health = await apiService.getHealthStatus();
      setHealthData(health);
      setStatus(health.status);
      setLastChecked(new Date());
    } catch (error) {
      setHealthData({ status: 'unhealthy', error: error.message });
      setStatus('unhealthy');
      setLastChecked(new Date());
    }
  };

  useEffect(() => {
    checkHealth();
    
    // Auto-refresh every 30 seconds
    const interval = setInterval(checkHealth, 30000);
    return () => clearInterval(interval);
  }, []);

  const getStatusIcon = () => {
    switch (status) {
      case 'healthy':
        return <CheckCircle className="h-5 w-5 text-green-500" />;
      case 'unhealthy':
        return <XCircle className="h-5 w-5 text-red-500" />;
      case 'loading':
        return <Clock className="h-5 w-5 text-yellow-500 animate-spin" />;
      default:
        return <WifiOff className="h-5 w-5 text-gray-400" />;
    }
  };

  const getStatusText = () => {
    switch (status) {
      case 'healthy':
        return 'API is running';
      case 'unhealthy':
        return 'API is down';
      case 'loading':
        return 'Checking...';
      default:
        return 'Unknown status';
    }
  };

  const getStatusColor = () => {
    switch (status) {
      case 'healthy':
        return 'text-green-600 bg-green-50 border-green-200';
      case 'unhealthy':
        return 'text-red-600 bg-red-50 border-red-200';
      case 'loading':
        return 'text-yellow-600 bg-yellow-50 border-yellow-200';
      default:
        return 'text-gray-600 bg-gray-50 border-gray-200';
    }
  };

  return (
    <div className="card">
      <div className="card-header">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <Wifi className="h-5 w-5 text-gray-500" />
            <h3 className="card-title text-lg">API Status</h3>
          </div>
          <button
            onClick={checkHealth}
            disabled={status === 'loading'}
            className="btn btn-sm btn-outline"
          >
            Refresh
          </button>
        </div>
      </div>
      <div className="card-content">
        <div className={`flex items-center space-x-3 p-4 rounded-lg border ${getStatusColor()}`}>
          {getStatusIcon()}
          <div className="flex-1">
            <p className="font-medium">{getStatusText()}</p>
            {healthData?.message && (
              <p className="text-sm opacity-75">{healthData.message}</p>
            )}
            {healthData?.responseTime && (
              <p className="text-sm opacity-75">
                Response time: {healthData.responseTime}ms
              </p>
            )}
            {healthData?.error && (
              <p className="text-sm opacity-75">{healthData.error}</p>
            )}
          </div>
        </div>
        
        {lastChecked && (
          <p className="text-xs text-gray-500 mt-2">
            Last checked: {lastChecked.toLocaleTimeString()}
          </p>
        )}
      </div>
    </div>
  );
};

export default ApiStatus; 