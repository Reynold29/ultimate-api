# Ultimate Guitar Tab Parser - Frontend

A modern, production-ready React frontend for the Ultimate Guitar Tab Parser API. This application provides a beautiful interface for parsing and extracting guitar tabs from Ultimate Guitar.

## 🚀 Features

- **Modern React 18** with hooks and functional components
- **Tailwind CSS** for beautiful, responsive design
- **Vite** for fast development and optimized builds
- **Axios** for robust API communication
- **React Router** for navigation
- **Lucide React** for beautiful icons
- **Production-ready** with proper error handling and loading states

## 📋 Prerequisites

- Node.js 16.0.0 or higher
- npm 8.0.0 or higher
- Ultimate Guitar Tab Parser API running (see backend README)

## 🛠️ Installation

1. **Navigate to the frontend directory:**
   ```bash
   cd ultimate-api/frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start the development server:**
   ```bash
   npm run dev
   ```

4. **Open your browser:**
   The application will open automatically at `http://localhost:3000`

## 🏗️ Project Structure

```
frontend/
├── public/                 # Static assets
├── src/
│   ├── components/         # React components
│   │   ├── Header.jsx     # Application header
│   │   ├── ApiStatus.jsx  # API health status
│   │   └── TabParser.jsx  # Main tab parser component
│   ├── config/
│   │   └── api.js         # API configuration
│   ├── services/
│   │   └── api.js         # API service layer
│   ├── App.jsx            # Main application component
│   ├── main.jsx           # Application entry point
│   └── index.css          # Global styles
├── package.json           # Dependencies and scripts
├── vite.config.js         # Vite configuration
├── tailwind.config.js     # Tailwind CSS configuration
└── README.md              # This file
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the frontend directory:

```env
# Development
VITE_API_URL=http://127.0.0.1:5000

# Production
VITE_API_URL=https://your-api-domain.com
```

### API Configuration

The API configuration is handled in `src/config/api.js`:

```javascript
const config = {
  development: {
    apiUrl: 'http://127.0.0.1:5000',
    timeout: 60000, // 60 seconds for development
  },
  production: {
    apiUrl: process.env.VITE_API_URL || 'https://api.yourdomain.com',
    timeout: 60000, // 60 seconds for production
  },
};
```

## 📦 Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint
- `npm run format` - Format code with Prettier

## 🎨 Styling

This project uses **Tailwind CSS** with custom components and utilities:

- **Custom color palette** with primary and secondary colors
- **Responsive design** that works on all devices
- **Custom animations** for smooth interactions
- **Component classes** for consistent styling

### Custom Components

```css
.btn          /* Base button styles */
.btn-primary  /* Primary button variant */
.btn-secondary /* Secondary button variant */
.card         /* Card container */
.input        /* Form input styles */
```

## 🔌 API Integration

The frontend communicates with the Ultimate Guitar Tab Parser API through the `ApiService` class:

### Key Methods

- `testConnection()` - Test API health
- `parseTab(url)` - Parse a single tab
- `parseMultipleTabs(urls)` - Parse multiple tabs
- `getHealthStatus()` - Get detailed health information

### Error Handling

The API service includes comprehensive error handling:

- Network errors
- API errors (4xx, 5xx)
- Timeout handling
- User-friendly error messages

## 🚀 Deployment

### Build for Production

```bash
npm run build
```

This creates a `dist` folder with optimized files ready for deployment.

### Deployment Options

1. **Netlify:**
   ```bash
   npm run build
   # Upload dist folder to Netlify
   ```

2. **Vercel:**
   ```bash
   npm run build
   # Deploy with Vercel CLI
   ```

3. **Static Hosting:**
   ```bash
   npm run build
   # Upload dist folder to any static hosting service
   ```

### Environment Setup

For production deployment, set the `VITE_API_URL` environment variable to your production API URL.

## 🧪 Testing

The project is set up for testing with:

- **ESLint** for code quality
- **Prettier** for code formatting
- **Vite** for fast development

To add testing:

```bash
npm install --save-dev vitest @testing-library/react @testing-library/jest-dom
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and linting
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

If you encounter any issues:

1. Check the browser console for errors
2. Verify the API server is running
3. Check the network tab for API requests
4. Review the configuration in `src/config/api.js`

## 🔗 Related

- [Backend API](../README.md) - Flask API documentation
- [API Client](../api_client.js) - JavaScript API client
- [Frontend Test](../frontend_test.html) - Simple HTML test page 

## 🚀 Netlify Deployment

To deploy the frontend to Netlify and connect it to your Railway backend:

1. **Build Command:** `npm run build`
2. **Publish Directory:** `dist`
3. **Set Environment Variable:**
   - Go to Site Settings > Environment Variables in Netlify
   - Add:
     - `VITE_API_URL=https://ultimate-api-production.up.railway.app`
4. **Deploy:**
   - Connect your GitHub repo and deploy, or drag-and-drop the `dist` folder after building locally.

This will ensure your frontend talks to your Railway backend in production. 