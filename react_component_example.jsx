import React, { useState, useEffect } from 'react';

/**
 * React Component for Ultimate Guitar Tab Parser
 * 
 * This component demonstrates how to use the Flask API in a React application.
 * You can copy this component and modify it for your needs.
 */

const UltimateGuitarTabParser = () => {
    const [apiStatus, setApiStatus] = useState('idle'); // 'idle', 'loading', 'success', 'error'
    const [apiMessage, setApiMessage] = useState('');
    const [tabUrl, setTabUrl] = useState('');
    const [tabData, setTabData] = useState(null);
    const [isParsing, setIsParsing] = useState(false);
    const [error, setError] = useState('');

    const API_BASE_URL = 'http://127.0.0.1:5000';

    // Test API connection on component mount
    useEffect(() => {
        testApiConnection();
    }, []);

    const testApiConnection = async () => {
        setApiStatus('loading');
        setError('');
        
        try {
            const response = await fetch(`${API_BASE_URL}/`);
            if (response.ok) {
                const data = await response.text();
                setApiStatus('success');
                setApiMessage(data);
            } else {
                setApiStatus('error');
                setError(`HTTP error! status: ${response.status}`);
            }
        } catch (err) {
            setApiStatus('error');
            setError(`Connection failed: ${err.message}`);
        }
    };

    const parseTab = async () => {
        if (!tabUrl.trim()) {
            setError('Please enter a URL');
            return;
        }

        setIsParsing(true);
        setError('');
        setTabData(null);

        try {
            const response = await fetch(`${API_BASE_URL}/tab?url=${encodeURIComponent(tabUrl)}`);
            const data = await response.json();

            if (response.ok) {
                setTabData(data);
            } else {
                setError(data.error || 'Failed to parse tab');
            }
        } catch (err) {
            setError(`Request failed: ${err.message}`);
        } finally {
            setIsParsing(false);
        }
    };

    const getStatusColor = () => {
        switch (apiStatus) {
            case 'success': return 'text-green-600';
            case 'error': return 'text-red-600';
            case 'loading': return 'text-yellow-600';
            default: return 'text-gray-600';
        }
    };

    const getStatusIcon = () => {
        switch (apiStatus) {
            case 'success': return '✅';
            case 'error': return '❌';
            case 'loading': return '⏳';
            default: return '⏸️';
        }
    };

    return (
        <div className="max-w-4xl mx-auto p-6 bg-white rounded-lg shadow-lg">
            <h1 className="text-3xl font-bold text-center mb-8 text-gray-800">
                🎸 Ultimate Guitar Tab Parser
            </h1>

            {/* API Status Section */}
            <div className="mb-8 p-6 border border-gray-200 rounded-lg">
                <h2 className="text-xl font-semibold mb-4 text-gray-700">
                    API Status
                </h2>
                <div className="flex items-center gap-3 mb-4">
                    <span className="text-2xl">{getStatusIcon()}</span>
                    <span className={`font-medium ${getStatusColor()}`}>
                        {apiStatus === 'idle' && 'Ready to test'}
                        {apiStatus === 'loading' && 'Testing connection...'}
                        {apiStatus === 'success' && 'API is running'}
                        {apiStatus === 'error' && 'Connection failed'}
                    </span>
                </div>
                
                {apiStatus === 'success' && (
                    <div className="bg-green-50 border border-green-200 rounded p-3">
                        <p className="text-green-800">
                            <strong>Response:</strong> {apiMessage}
                        </p>
                    </div>
                )}
                
                {apiStatus === 'error' && (
                    <div className="bg-red-50 border border-red-200 rounded p-3">
                        <p className="text-red-800">
                            <strong>Error:</strong> {error}
                        </p>
                    </div>
                )}
                
                <button
                    onClick={testApiConnection}
                    disabled={apiStatus === 'loading'}
                    className="mt-4 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 disabled:bg-gray-400 disabled:cursor-not-allowed"
                >
                    {apiStatus === 'loading' ? 'Testing...' : 'Test Connection'}
                </button>
            </div>

            {/* Tab Parser Section */}
            <div className="mb-8 p-6 border border-gray-200 rounded-lg">
                <h2 className="text-xl font-semibold mb-4 text-gray-700">
                    Parse Ultimate Guitar Tab
                </h2>
                
                <div className="mb-4">
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                        Ultimate Guitar Tab URL:
                    </label>
                    <input
                        type="text"
                        value={tabUrl}
                        onChange={(e) => setTabUrl(e.target.value)}
                        placeholder="https://tabs.ultimate-guitar.com/tab/artist/song-name-123456"
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                </div>

                <div className="mb-4 p-3 bg-gray-50 rounded text-sm text-gray-600">
                    <strong>Example:</strong> https://tabs.ultimate-guitar.com/tab/artist/song-name-123456
                </div>

                <button
                    onClick={parseTab}
                    disabled={isParsing || !tabUrl.trim()}
                    className="px-6 py-2 bg-green-500 text-white rounded hover:bg-green-600 disabled:bg-gray-400 disabled:cursor-not-allowed"
                >
                    {isParsing ? 'Parsing...' : 'Parse Tab'}
                </button>

                {error && (
                    <div className="mt-4 p-3 bg-red-50 border border-red-200 rounded">
                        <p className="text-red-800">{error}</p>
                    </div>
                )}

                {tabData && (
                    <div className="mt-6">
                        <h3 className="text-lg font-semibold mb-3 text-gray-700">
                            Parsed Tab Data:
                        </h3>
                        <div className="bg-gray-50 border border-gray-200 rounded p-4 max-h-96 overflow-y-auto">
                            <pre className="text-sm text-gray-800 whitespace-pre-wrap">
                                {JSON.stringify(tabData, null, 2)}
                            </pre>
                        </div>
                    </div>
                )}
            </div>

            {/* Usage Instructions */}
            <div className="p-6 bg-blue-50 border border-blue-200 rounded-lg">
                <h3 className="text-lg font-semibold mb-3 text-blue-800">
                    How to Use This Component:
                </h3>
                <ol className="list-decimal list-inside space-y-2 text-blue-700">
                    <li>Make sure your Flask API server is running on <code className="bg-blue-100 px-1 rounded">http://127.0.0.1:5000</code></li>
                    <li>Test the API connection using the "Test Connection" button</li>
                    <li>Enter an Ultimate Guitar tab URL in the input field</li>
                    <li>Click "Parse Tab" to extract the tab data</li>
                    <li>The parsed data will be displayed in JSON format</li>
                </ol>
            </div>
        </div>
    );
};

export default UltimateGuitarTabParser;

// Usage in your React app:
/*
import UltimateGuitarTabParser from './UltimateGuitarTabParser';

function App() {
    return (
        <div className="min-h-screen bg-gray-100 py-8">
            <UltimateGuitarTabParser />
        </div>
    );
}
*/ 