import { useState } from 'react';
import { Search, Music, Download, Copy, ExternalLink, AlertCircle, Users } from 'lucide-react';
import { apiService } from '../services/api.js';

const SongSearch = () => {
  const [songName, setSongName] = useState('');
  const [artistName, setArtistName] = useState('');
  const [searchResult, setSearchResult] = useState(null);
  const [isSearching, setIsSearching] = useState(false);
  const [error, setError] = useState('');
  const [copied, setCopied] = useState(false);

  const searchSong = async () => {
    if (!songName.trim()) {
      setError('Please enter a song name');
      return;
    }

    setIsSearching(true);
    setError('');
    setSearchResult(null);
    setCopied(false);

    try {
      const data = await apiService.searchSong(songName.trim(), artistName.trim());
      setSearchResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setIsSearching(false);
    }
  };

  const copyToClipboard = async () => {
    if (!searchResult) return;
    
    try {
      await navigator.clipboard.writeText(JSON.stringify(searchResult, null, 2));
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (err) {
      // Silent fail for clipboard operations
    }
  };

  const openUrl = () => {
    if (searchResult?.url) {
      window.open(searchResult.url, '_blank');
    }
  };

  return (
    <div className="space-y-6">
      {/* Input Section */}
      <div className="card">
        <div className="card-header">
          <div className="flex items-center space-x-2">
            <Search className="h-5 w-5 text-primary-600" />
            <h3 className="card-title">Search Songs by Name</h3>
          </div>
          <p className="card-description">
            Search for any song and get the Ultimate Guitar URL automatically
          </p>
        </div>
        <div className="card-content">
          <div className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label htmlFor="songName" className="block text-sm font-medium text-gray-700 mb-2">
                  Song Name *
                </label>
                <input
                  id="songName"
                  type="text"
                  value={songName}
                  onChange={(e) => setSongName(e.target.value)}
                  placeholder="e.g., Wonderwall, Shape of You, What an Awesome God"
                  className="input"
                  disabled={isSearching}
                  onKeyPress={(e) => e.key === 'Enter' && searchSong()}
                />
              </div>
              
              <div>
                <label htmlFor="artistName" className="block text-sm font-medium text-gray-700 mb-2">
                  Artist Name (Optional)
                </label>
                <input
                  id="artistName"
                  type="text"
                  value={artistName}
                  onChange={(e) => setArtistName(e.target.value)}
                  placeholder="e.g., Oasis, Ed Sheeran, Phil Wickham"
                  className="input"
                  disabled={isSearching}
                  onKeyPress={(e) => e.key === 'Enter' && searchSong()}
                />
              </div>
            </div>
            
            <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
              <div className="flex items-start space-x-2">
                <Music className="h-4 w-4 text-blue-600 mt-0.5 flex-shrink-0" />
                <div className="text-sm text-blue-800">
                  <p className="font-medium mb-1">How it works:</p>
                  <ul className="space-y-1 text-xs">
                    <li>• Enter a song name (artist name is optional but helps accuracy)</li>
                    <li>• We'll find the best Ultimate Guitar URL for the song</li>
                    <li>• Get the URL to use in your music apps and chord apps!</li>
                    <li>• Perfect for Flutter apps and other music applications</li>
                  </ul>
                </div>
              </div>
            </div>

            <div className="flex space-x-3">
              <button
                onClick={searchSong}
                disabled={isSearching || !songName.trim()}
                className="btn btn-primary btn-lg flex-1"
              >
                {isSearching ? (
                  <>
                    <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                    Searching...
                  </>
                ) : (
                  <>
                    <Search className="h-4 w-4 mr-2" />
                    Search Song
                  </>
                )}
              </button>
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
      {searchResult && (
        <div className="card animate-fade-in">
          <div className="card-header">
            <div className="flex items-center justify-between">
              <div>
                <h3 className="card-title">
                  {searchResult.song_name}
                  {searchResult.artist_name && (
                    <span className="text-gray-500 font-normal"> by {searchResult.artist_name}</span>
                  )}
                </h3>
                <p className="card-description">
                  Found Ultimate Guitar URL
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
                {searchResult.url && (
                  <button
                    onClick={openUrl}
                    className="btn btn-sm btn-primary"
                    title="Open Ultimate Guitar URL"
                  >
                    <ExternalLink className="h-4 w-4 mr-1" />
                    Open Tab
                  </button>
                )}
              </div>
            </div>
          </div>
          <div className="card-content">
            <div className="space-y-4">
              {/* URL Display */}
              {searchResult.url && (
                <div className="bg-gray-50 rounded-lg p-4">
                  <div className="flex items-center space-x-2 mb-3">
                    <ExternalLink className="h-4 w-4 text-gray-600" />
                    <h4 className="font-medium text-gray-900">Ultimate Guitar URL</h4>
                  </div>
                  <div className="bg-white border border-gray-200 rounded p-3">
                    <a 
                      href={searchResult.url} 
                      target="_blank" 
                      rel="noopener noreferrer"
                      className="text-blue-600 hover:text-blue-800 break-all"
                    >
                      {searchResult.url}
                    </a>
                  </div>
                </div>
              )}

              {/* Message */}
              {searchResult.message && (
                <div className="bg-green-50 border border-green-200 rounded-lg p-4">
                  <div className="flex items-start space-x-2">
                    <div className="w-5 h-5 bg-green-100 rounded-full flex items-center justify-center flex-shrink-0 mt-0.5">
                      <div className="w-2 h-2 bg-green-600 rounded-full"></div>
                    </div>
                    <div className="text-sm text-green-800">
                      <p className="font-medium">Success!</p>
                      <p>{searchResult.message}</p>
                    </div>
                  </div>
                </div>
              )}

              {/* Raw JSON */}
              <details className="group">
                <summary className="cursor-pointer text-sm font-medium text-gray-700 hover:text-gray-900">
                  Raw JSON Response
                </summary>
                <div className="mt-3 p-4 bg-gray-50 rounded-lg">
                  <pre className="text-xs text-gray-800 overflow-x-auto">
                    {JSON.stringify(searchResult, null, 2)}
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

export default SongSearch; 