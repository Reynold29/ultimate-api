import { Guitar, Github, ExternalLink } from 'lucide-react';

const Header = () => {
  return (
    <header className="bg-white shadow-sm border-b">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo and Title */}
          <div className="flex items-center space-x-3">
            <div className="flex-shrink-0">
              <Guitar className="h-8 w-8 text-primary-600" />
            </div>
            <div>
              <h1 className="text-xl font-bold text-gray-900">
                Ultimate Guitar Tab Parser
              </h1>
              <p className="text-sm text-gray-500">
                Parse and extract guitar tabs from Ultimate Guitar
              </p>
            </div>
          </div>

          {/* Navigation and Actions */}
          <div className="flex items-center space-x-4">
            <a
              href="https://github.com/yourusername/ultimate-guitar-tab-parser"
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center px-3 py-2 text-sm font-medium text-gray-700 hover:text-gray-900 transition-colors"
            >
              <Github className="h-4 w-4 mr-2" />
              GitHub
            </a>
            <a
              href="https://tabs.ultimate-guitar.com"
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center px-3 py-2 text-sm font-medium text-gray-700 hover:text-gray-900 transition-colors"
            >
              <ExternalLink className="h-4 w-4 mr-2" />
              Ultimate Guitar
            </a>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header; 