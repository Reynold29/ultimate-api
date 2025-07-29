import { Routes, Route } from 'react-router-dom';
import Header from './components/Header.jsx';
import ApiStatus from './components/ApiStatus.jsx';
import TabParser from './components/TabParser.jsx';

function App() {
  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <Routes>
          <Route 
            path="/" 
            element={
              <div className="space-y-8">
                <div className="text-center">
                  <h1 className="text-4xl font-bold text-gray-900 mb-4">
                    Ultimate Guitar Tab Parser
                  </h1>
                  <p className="text-xl text-gray-600 max-w-3xl mx-auto">
                    Extract and parse guitar tabs from Ultimate Guitar with this New and Powerful API. 
                    Get structured JSON data for your music applications.
                  </p>
                </div>
                
                <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                  {/* API Status */}
                  <div className="lg:col-span-1">
                    <ApiStatus />
                  </div>
                  
                  {/* Tab Parser */}
                  <div className="lg:col-span-2">
                    <TabParser />
                  </div>
                </div>
                
                {/* Features Section */}
                <div className="mt-16">
                  <h2 className="text-2xl font-bold text-gray-900 text-center mb-8">
                    Features
                  </h2>
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                    <div className="card text-center">
                      <div className="card-content">
                        <div className="w-12 h-12 bg-primary-100 rounded-lg flex items-center justify-center mx-auto mt-8 mb-6">
                          <svg className="w-6 h-6 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                          </svg>
                        </div>
                        <h3 className="font-semibold text-gray-900 mb-2">Fast Parsing</h3>
                        <p className="text-gray-600 text-sm">
                          Extract tab data in seconds with the optimized parsing engine
                        </p>
                      </div>
                    </div>
                    
                    <div className="card text-center">
                      <div className="card-content">
                        <div className="w-12 h-12 bg-primary-100 rounded-lg flex items-center justify-center mx-auto mt-8 mb-6">
                          <svg className="w-6 h-6 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                          </svg>
                        </div>
                        <h3 className="font-semibold text-gray-900 mb-2">Structured Data</h3>
                        <p className="text-gray-600 text-sm">
                          Get clean, structured JSON with chords, lyrics, and metadata
                        </p>
                      </div>
                    </div>
                    
                    <div className="card text-center">
                      <div className="card-content">
                        <div className="w-12 h-12 bg-primary-100 rounded-lg flex items-center justify-center mx-auto mt-8 mb-6">
                          <svg className="w-6 h-6 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8.684 13.342C8.886 12.938 9 12.482 9 12c0-.482-.114-.938-.316-1.342m0 2.684a3 3 0 110-2.684m0 2.684l6.632 3.316m-6.632-6l6.632-3.316m0 0a3 3 0 105.367-2.684 3 3 0 00-5.367 2.684zm0 9.316a3 3 0 105.367 2.684 3 3 0 00-5.367-2.684z" />
                          </svg>
                        </div>
                        <h3 className="font-semibold text-gray-900 mb-2">API Ready</h3>
                        <p className="text-gray-600 text-sm">
                          RESTful API perfect for integration with any applications
                        </p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            } 
          />
        </Routes>
      </main>
      
      <footer className="bg-white border-t mt-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="text-center text-gray-600">
            <p>&copy; 2024 Ultimate Guitar Tab Parser. Built with React and Flask.</p>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default App; 