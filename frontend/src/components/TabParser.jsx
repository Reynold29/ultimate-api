import { useState } from 'react';
import { Guitar, Download, Copy, ExternalLink, AlertCircle } from 'lucide-react';
import { apiService } from '../services/api.js';

const TabParser = () => {
  const [tabUrl, setTabUrl] = useState('');
  const [tabData, setTabData] = useState(null);
  const [isParsing, setIsParsing] = useState(false);
  const [error, setError] = useState('');
  const [copied, setCopied] = useState(false);

  const parseTab = async () => {
    if (!tabUrl.trim()) {
      setError('Please enter a URL');
      return;
    }

    setIsParsing(true);
    setError('');
    setTabData(null);
    setCopied(false);

    try {
      const data = await apiService.parseTab(tabUrl);
      setTabData(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setIsParsing(false);
    }
  };

  const copyToClipboard = async () => {
    if (!tabData) return;
    
    try {
      await navigator.clipboard.writeText(JSON.stringify(tabData, null, 2));
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (err) {
      console.error('Failed to copy:', err);
    }
  };

  const downloadJson = () => {
    if (!tabData) return;
    
    const dataStr = JSON.stringify(tabData, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(dataBlob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `${tabData.title || 'tab'}-${tabData.artist_name || 'unknown'}.json`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  };

  const openOriginalUrl = () => {
    if (tabUrl) {
      window.open(tabUrl, '_blank');
    }
  };

  return (
    <div className="space-y-6">
      {/* Input Section */}
      <div className="card">
        <div className="card-header">
          <div className="flex items-center space-x-2">
            <Guitar className="h-5 w-5 text-primary-600" />
            <h3 className="card-title">Parse Ultimate Guitar Tab</h3>
          </div>
          <p className="card-description">
            Enter an Ultimate Guitar tab URL to extract the tab data
          </p>
        </div>
        <div className="card-content">
          <div className="space-y-4">
            <div>
              <label htmlFor="tabUrl" className="block text-sm font-medium text-gray-700 mb-2">
                Ultimate Guitar Tab URL
              </label>
              <input
                id="tabUrl"
                type="url"
                value={tabUrl}
                onChange={(e) => setTabUrl(e.target.value)}
                placeholder="https://tabs.ultimate-guitar.com/tab/artist/song-name-123456"
                className="input"
                disabled={isParsing}
              />
            </div>
            
            <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
              <div className="flex items-start space-x-2">
                <ExternalLink className="h-4 w-4 text-blue-600 mt-0.5 flex-shrink-0" />
                <div className="text-sm text-blue-800">
                  <p className="font-medium mb-1">Example URLs:</p>
                  <ul className="space-y-1 text-xs">
                    <li>• https://tabs.ultimate-guitar.com/tab/ed-sheeran/shape-of-you-123456</li>
                    <li>• https://tabs.ultimate-guitar.com/tab/beatles/let-it-be-789012</li>
                  </ul>
                </div>
              </div>
            </div>

            <div className="flex space-x-3">
              <button
                onClick={parseTab}
                disabled={isParsing || !tabUrl.trim()}
                className="btn btn-primary btn-lg flex-1"
              >
                {isParsing ? (
                  <>
                    <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                    Parsing...
                  </>
                ) : (
                  'Parse Tab'
                )}
              </button>
              
              {tabUrl && (
                <button
                  onClick={openOriginalUrl}
                  className="btn btn-outline btn-lg"
                  title="Open original URL"
                >
                  <ExternalLink className="h-4 w-4" />
                </button>
              )}
            </div>

            {error && (
              <div className="flex items-start space-x-2 p-4 bg-red-50 border border-red-200 rounded-lg">
                <AlertCircle className="h-5 w-5 text-red-600 mt-0.5 flex-shrink-0" />
                <div className="text-sm text-red-800">
                  <p className="font-medium">Error</p>
                  <p>{error}</p>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Results Section */}
      {tabData && (
        <div className="card animate-fade-in">
          <div className="card-header">
            <div className="flex items-center justify-between">
              <div>
                <h3 className="card-title">{tabData.title || 'Untitled'}</h3>
                <p className="card-description">
                  by {tabData.artist_name || 'Unknown Artist'}
                </p>
              </div>
              <div className="flex space-x-2">
                <button
                  onClick={copyToClipboard}
                  className="btn btn-sm btn-outline"
                  title="Copy JSON to clipboard"
                >
                  <Copy className="h-4 w-4 mr-1" />
                  {copied ? 'Copied!' : 'Copy'}
                </button>
                <button
                  onClick={downloadJson}
                  className="btn btn-sm btn-primary"
                  title="Download JSON file"
                >
                  <Download className="h-4 w-4 mr-1" />
                  Download
                </button>
              </div>
            </div>
          </div>
          <div className="card-content">
            <div className="space-y-4">
              {/* Tab Info */}
              {(tabData.difficulty || tabData.key || tabData.capo || tabData.tuning) && (
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4 p-4 bg-gray-50 rounded-lg">
                  {tabData.difficulty && (
                    <div>
                      <p className="text-xs font-medium text-gray-500 uppercase">Difficulty</p>
                      <p className="text-sm font-medium">{tabData.difficulty}</p>
                    </div>
                  )}
                  {tabData.key && (
                    <div>
                      <p className="text-xs font-medium text-gray-500 uppercase">Key</p>
                      <p className="text-sm font-medium">{tabData.key}</p>
                    </div>
                  )}
                  {tabData.capo && (
                    <div>
                      <p className="text-xs font-medium text-gray-500 uppercase">Capo</p>
                      <p className="text-sm font-medium">{tabData.capo}</p>
                    </div>
                  )}
                  {tabData.tuning && (
                    <div>
                      <p className="text-xs font-medium text-gray-500 uppercase">Tuning</p>
                      <p className="text-sm font-medium">{tabData.tuning}</p>
                    </div>
                  )}
                </div>
              )}

              {/* Tab Content */}
              <div>
                <h4 className="text-sm font-medium text-gray-700 mb-3">Tab Content</h4>
                <div className="bg-gray-900 text-green-400 p-4 rounded-lg font-mono text-sm overflow-x-auto max-h-96 overflow-y-auto">
                  {tabData.lines?.map((line, index) => (
                    <div key={index} className="whitespace-pre">
                      {line.lyric && <span>{line.lyric}</span>}
                      {line.chords && (
                        <span className="text-yellow-400">
                          {line.chords.map((chord, chordIndex) => (
                            <span key={chordIndex}>
                              {' '.repeat(chord.pre_spaces)}{chord.note}
                            </span>
                          ))}
                        </span>
                      )}
                      {!line.lyric && !line.chords && <span>&nbsp;</span>}
                    </div>
                  ))}
                </div>
              </div>

              {/* Raw JSON */}
              <details className="group">
                <summary className="cursor-pointer text-sm font-medium text-gray-700 hover:text-gray-900">
                  Raw JSON Data
                </summary>
                <div className="mt-3 p-4 bg-gray-50 rounded-lg">
                  <pre className="text-xs text-gray-800 overflow-x-auto">
                    {JSON.stringify(tabData, null, 2)}
                  </pre>
                </div>
              </details>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default TabParser; 