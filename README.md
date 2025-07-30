# Ultimate Guitar Tab Parser

A powerful API and frontend application for parsing and extracting guitar tabs from Ultimate Guitar. This project includes both a Flask backend API and a modern React frontend.

## 🎸 Features

- **Flask API** - RESTful API for parsing Ultimate Guitar tabs
- **React Frontend** - Modern, responsive web interface
- **Tab Extraction** - Extract chords, lyrics, and metadata
- **JSON Output** - Structured data for easy integration
- **Production Ready** - Proper error handling, CORS, and deployment configs

## 📁 Project Structure

```
ultimate-api/
├── server/                 # Flask API backend
│   ├── __init__.py        # Flask app initialization
│   ├── views.py           # API endpoints
│   ├── parser.py          # HTML parsing logic
│   ├── tab_parser.py      # Tab extraction utilities
│   └── tab.py             # Tab data structures
├── frontend/              # React frontend application
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── config/        # API configuration
│   │   ├── services/      # API service layer
│   │   └── ...
│   ├── package.json       # Frontend dependencies
│   └── README.md          # Frontend documentation
├── api_client.js          # JavaScript API client
├── frontend_test.html     # Simple HTML test page
├── requirements.txt       # Python dependencies
├── run.py                 # Flask server entry point
└── README.md              # This file
```

## 🚀 Quick Start

### Backend (Flask API)

1. **Install Python dependencies:**
   ```bash
   cd ultimate-api
   source venv/bin/activate  # or create new venv
   pip install -r requirements.txt
   ```

2. **Start the Flask server:**
   ```bash
   python run.py
   ```

3. **Test the API:**
   - Visit `https://ultimate-api-production.up.railway.app/` for status
   - Use `/tab?url=<ultimate_guitar_url>` to parse tabs

### Frontend (React App)

1. **Install Node.js dependencies:**
   ```bash
   cd ultimate-api/frontend
   npm install
   ```

2. **Start the development server:**
   ```bash
   npm run dev
   ```

3. **Open in browser:**
   The app will open at `http://localhost:3000`

## 🔌 API Endpoints

### GET `/`
Returns API status message.

**Response:**
```
The API Server is running
```

### GET `/tab?url=<ultimate_guitar_url>`
Parses an Ultimate Guitar tab URL and returns structured data.

**Parameters:**
- `url` (required): Ultimate Guitar tab URL

**Response:**
```json
{
  "title": "Song Title",
  "artist_name": "Artist Name",
  "author": "Tab Author",
  "difficulty": "Intermediate",
  "key": "C",
  "capo": "2nd fret",
  "tuning": "Standard",
  "lines": [
    {
      "lyric": "Song lyrics here"
    },
    {
      "chords": [
        {
          "note": "G",
          "pre_spaces": 8
        }
      ]
    }
  ]
}
```

## 🎨 Frontend Features

- **Modern UI** - Beautiful, responsive design with Tailwind CSS
- **Real-time Status** - API health monitoring with auto-refresh
- **Tab Parsing** - Easy URL input and tab extraction
- **Data Export** - Copy to clipboard and download JSON
- **Error Handling** - User-friendly error messages
- **Mobile Responsive** - Works on all devices

## 🛠️ Development

### Backend Development

The Flask API is located in the `server/` directory:

- `views.py` - API endpoints and request handling
- `parser.py` - HTML parsing and tab extraction logic
- `tab_parser.py` - High-level tab parsing functions
- `tab.py` - Data structures for tab representation

### Frontend Development

The React frontend is in the `frontend/` directory:

- `src/components/` - Reusable React components
- `src/services/` - API communication layer
- `src/config/` - Environment and API configuration

## 🚀 Deployment

### Backend Deployment

1. **Production server setup:**
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 run:app
   ```

2. **Environment variables:**
   ```bash
   export FLASK_ENV=production
   export FLASK_APP=run.py
   ```

### Frontend Deployment

1. **Build for production:**
   ```bash
   cd frontend
   npm run build
   ```

2. **Deploy options:**
   - **Netlify:** Upload `dist` folder or connect GitHub repo
   - **Vercel:** Deploy with Vercel CLI
   - **Static hosting:** Upload `dist` folder to any static host

3. **Environment setup:**
   ```bash
   VITE_API_URL=https://your-api-domain.com
   ```

## 📚 Documentation

- [Frontend Documentation](frontend/README.md) - Complete frontend guide
- [API Client](api_client.js) - JavaScript API client usage
- [Frontend Test](frontend_test.html) - Simple HTML test page

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test both backend and frontend
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For issues and questions:

1. Check the browser console for frontend errors
2. Check the Flask server logs for backend errors
3. Verify API connectivity
4. Review the configuration files

## 🔗 Related Projects

- [Ultimate Guitar](https://tabs.ultimate-guitar.com) - Source of guitar tabs
- [React](https://reactjs.org) - Frontend framework
- [Flask](https://flask.palletsprojects.com) - Backend framework
- [Tailwind CSS](https://tailwindcss.com) - Styling framework

# Railway Deployment (Backend)

## How to Deploy on Railway

1. **Ensure your dependencies are in `requirements.txt`.**
2. **Your backend entrypoint is `run.py`, which starts the Flask server.**
3. **Railway will automatically set the `PORT` environment variable.**
   - The code already uses `os.environ.get('PORT', 5000)`.
4. **Add a `Procfile` with the following content:**

   ```
   web: python run.py
   ```

5. **Deploy to Railway:**
   - Push your code to GitHub.
   - Create a new Railway project and link your GitHub repo.
   - Railway will auto-detect Python and install dependencies.
   - The backend will be available at the Railway-provided URL.

## Notes
- If you use Selenium, ensure you use a Railway plan that supports Docker or custom images, as browser automation may not work on the free tier.
- For static Flask APIs, the default setup is sufficient.
