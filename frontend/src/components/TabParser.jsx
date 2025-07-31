import { useState } from 'react';
import { Guitar, Download, Copy, ExternalLink, AlertCircle } from 'lucide-react';
import { apiService } from '../services/api.js';

const TabParser = () => {
  const [tabUrl, setTabUrl] = useState('');
  const [tabData, setTabData] = useState(null);
  const [combinedData, setCombinedData] = useState(null);
  const [isParsing, setIsParsing] = useState(false);
  const [error, setError] = useState('');
  const [copied, setCopied] = useState(false);
  const [activeTab, setActiveTab] = useState('lyrics');

  const parseTab = async () => {
    if (!tabUrl.trim()) {
      setError('Please enter a URL');
      return;
    }

    setIsParsing(true);
    setError('');
    setTabData(null);
    setCombinedData(null);
    setCopied(false);

    try {
      // Parse regular tab data
      const data = await apiService.parseTab(tabUrl);
      setTabData(data);
      
      // Also fetch combined data
      try {
        const combined = await apiService.parseCombinedTab(tabUrl);
        setCombinedData(combined);
      } catch (combinedErr) {
        console.log('Combined format not available:', combinedErr.message);
      }
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
      // Silent fail for clipboard operations
    }
  };

  const downloadTabContent = () => {
    if (!tabData) return;
    
    // Create content from lyrics and tabs
    let content = '';
    if (tabData.lyrics_text) {
      content += tabData.lyrics_text;
    }
    if (tabData.lyrics_text && tabData.tabs_text) {
      content += '\n\n';
    }
    if (tabData.tabs_text) {
      content += tabData.tabs_text;
    }
    
    const dataBlob = new Blob([content], { type: 'text/plain' });
    const url = URL.createObjectURL(dataBlob);
    const link = document.createElement('a');
    link.href = url;
    
    // Generate filename from URL or use default
    const urlParts = tabUrl.split('/');
    const filename = urlParts.length > 2 ? urlParts.slice(-2).join('-') : 'tab-content';
    link.download = `${filename}.txt`;
    
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
                <h3 className="card-title">Parsed Tab Data</h3>
                <p className="card-description">
                  {tabData.blocks?.length || 0} blocks extracted
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
                  onClick={downloadTabContent}
                  className="btn btn-sm btn-primary"
                  title="Download Tab Content"
                >
                  <Download className="h-4 w-4 mr-1" />
                  Download Tab
                </button>
              </div>
            </div>
          </div>
          <div className="card-content">
            <div className="space-y-4">
              {/* Check for errors */}
              {tabData.blocks?.some(block => block.error) && (
                <div className="flex items-start space-x-2 p-4 bg-red-50 border border-red-200 rounded-lg">
                  <AlertCircle className="h-5 w-5 text-red-600 mt-0.5 flex-shrink-0" />
                  <div className="text-sm text-red-800">
                    <p className="font-medium">Parsing Errors</p>
                    {tabData.blocks.map((block, index) => 
                      block.error && <p key={index}>{block.error}</p>
                    )}
                  </div>
                </div>
              )}

              {/* Tabbed Content */}
              <div>
                <div className="flex border-b border-gray-200 mb-2">
                  <button
                    className={`px-4 py-2 -mb-px font-medium border-b-2 transition-colors duration-150 ${activeTab === 'lyrics' ? 'border-blue-600 text-blue-600' : 'border-transparent text-gray-500 hover:text-blue-600'}`}
                    onClick={() => setActiveTab('lyrics')}
                  >
                    Lyrics
                  </button>
                  <button
                    className={`px-4 py-2 -mb-px font-medium border-b-2 transition-colors duration-150 ${activeTab === 'tabs' ? 'border-blue-600 text-blue-600' : 'border-transparent text-gray-500 hover:text-blue-600'}`}
                    onClick={() => setActiveTab('tabs')}
                  >
                    Tabs
                  </button>
                  <button
                    className={`px-4 py-2 -mb-px font-medium border-b-2 transition-colors duration-150 ${activeTab === 'combined' ? 'border-blue-600 text-blue-600' : 'border-transparent text-gray-500 hover:text-blue-600'}`}
                    onClick={() => setActiveTab('combined')}
                  >
                    Combined
                  </button>
                </div>
                <div>
                  {activeTab === 'lyrics' && (
                    <pre className="bg-gray-900 text-green-400 p-4 rounded-lg font-mono text-sm overflow-x-auto max-h-96 overflow-y-auto whitespace-pre-wrap">
                      {tabData.lyrics_text || 'No lyrics found.'}
                    </pre>
                  )}
                  {activeTab === 'tabs' && (
                    <pre className="bg-gray-900 text-green-400 p-4 rounded-lg font-mono text-sm overflow-x-auto max-h-96 overflow-y-auto whitespace-pre-wrap">
                      {tabData.tabs_text || 'No tabs found.'}
                    </pre>
                  )}
                  {activeTab === 'combined' && (
                    <div className="bg-gray-900 text-green-400 p-4 rounded-lg font-mono text-sm overflow-x-auto max-h-96 overflow-y-auto">
                      {combinedData?.lines ? (
                        <div className="space-y-2">
                          {combinedData.lines.map((line, index) => (
                            <div key={index} className="whitespace-pre-wrap">
                              {line.chords && (
                                <div className="text-yellow-400 font-semibold">
                                  {line.chords}
                                </div>
                              )}
                              {line.lyric && (
                                <div className="text-green-400">
                                  {line.lyric}
                                </div>
                              )}
                              {!line.chords && !line.lyric && <br />}
                            </div>
                          ))}
                        </div>
                      ) : (
                        <div className="text-gray-400">
                          Combined format not available. Try parsing again.
                        </div>
                      )}
                    </div>
                  )}
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