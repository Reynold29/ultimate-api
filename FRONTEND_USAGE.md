# Ultimate Guitar Tab Parser - Frontend Usage Guide

This guide shows you how to use your Flask API in different frontend environments.

## 🚀 Quick Start

Your Flask API is running on `http://127.0.0.1:5000` and provides two endpoints:

1. **GET `/`** - Returns "hi" (API status check)
2. **GET `/tab?url=<ultimate_guitar_url>`** - Parses Ultimate Guitar tabs

## 📁 Available Frontend Examples

### 1. Simple HTML Test Page
**File:** `frontend_test.html`

A standalone HTML page you can open directly in your browser to test the API.

**How to use:**
```bash
# Make sure your Flask server is running
cd ultimate-api
python run.py

# Open the HTML file in your browser
open frontend_test.html
```

### 2. JavaScript API Client
**File:** `api_client.js`

A reusable JavaScript class that you can import into any frontend project.

**Features:**
- Test API connection
- Parse single tabs
- Parse multiple tabs in batch
- Error handling
- Works in browsers and Node.js

**Usage:**
```javascript
// Import the client
import UltimateGuitarApiClient from './api_client.js';

// Create instance
const apiClient = new UltimateGuitarApiClient();

// Test connection
apiClient.testConnection()
    .then(response => console.log('API is running:', response))
    .catch(error => console.error('API error:', error));

// Parse a tab
apiClient.parseTab('https://tabs.ultimate-guitar.com/tab/artist/song-name-123456')
    .then(tabData => console.log('Parsed tab:', tabData))
    .catch(error => console.error('Parse error:', error));
```

### 3. React Component
**File:** `react_component_example.jsx`

A complete React component with UI for testing and using the API.

**Features:**
- Real-time API status checking
- Tab URL input and parsing
- Error handling and loading states
- Beautiful UI with Tailwind CSS classes
- JSON data display

**Usage:**
```jsx
import UltimateGuitarTabParser from './react_component_example.jsx';

function App() {
    return (
        <div className="min-h-screen bg-gray-100 py-8">
            <UltimateGuitarTabParser />
        </div>
    );
}
```

## 🔧 Integration Examples

### Vanilla JavaScript
```javascript
// Simple fetch example
async function testApi() {
    try {
        const response = await fetch('http://127.0.0.1:5000/');
        const data = await response.text();
        console.log('API Response:', data);
    } catch (error) {
        console.error('Error:', error);
    }
}

async function parseTab(url) {
    try {
        const response = await fetch(`http://127.0.0.1:5000/tab?url=${encodeURIComponent(url)}`);
        const data = await response.json();
        console.log('Tab Data:', data);
    } catch (error) {
        console.error('Error:', error);
    }
}
```

### React with Hooks
```jsx
import { useState, useEffect } from 'react';

function TabParser() {
    const [tabData, setTabData] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    const parseTab = async (url) => {
        setLoading(true);
        setError('');
        
        try {
            const response = await fetch(`http://127.0.0.1:5000/tab?url=${encodeURIComponent(url)}`);
            const data = await response.json();
            
            if (response.ok) {
                setTabData(data);
            } else {
                setError(data.error || 'Failed to parse tab');
            }
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div>
            <button 
                onClick={() => parseTab('https://tabs.ultimate-guitar.com/tab/artist/song-123456')}
                disabled={loading}
            >
                {loading ? 'Parsing...' : 'Parse Tab'}
            </button>
            
            {error && <div className="error">{error}</div>}
            {tabData && <pre>{JSON.stringify(tabData, null, 2)}</pre>}
        </div>
    );
}
```

### Vue.js
```vue
<template>
  <div>
    <input v-model="tabUrl" placeholder="Enter Ultimate Guitar URL" />
    <button @click="parseTab" :disabled="loading">
      {{ loading ? 'Parsing...' : 'Parse Tab' }}
    </button>
    <div v-if="error" class="error">{{ error }}</div>
    <pre v-if="tabData">{{ JSON.stringify(tabData, null, 2) }}</pre>
  </div>
</template>

<script>
export default {
  data() {
    return {
      tabUrl: '',
      tabData: null,
      loading: false,
      error: ''
    };
  },
  methods: {
    async parseTab() {
      this.loading = true;
      this.error = '';
      
      try {
        const response = await fetch(`http://127.0.0.1:5000/tab?url=${encodeURIComponent(this.tabUrl)}`);
        const data = await response.json();
        
        if (response.ok) {
          this.tabData = data;
        } else {
          this.error = data.error || 'Failed to parse tab';
        }
      } catch (err) {
        this.error = err.message;
      } finally {
        this.loading = false;
      }
    }
  }
};
</script>
```

## 🌐 CORS Configuration

If you're getting CORS errors, you may need to enable CORS in your Flask app. Add this to your `server/__init__.py`:

```python
from flask import Flask
from flask_cors import CORS  # You'll need to install flask-cors

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Import views
import server.views
```

Install flask-cors:
```bash
pip install flask-cors
```

## 📝 API Response Format

The `/tab` endpoint returns JSON data with the parsed tab information. The exact structure depends on the tab content, but typically includes:

```json
{
  "title": "Song Title",
  "artist": "Artist Name",
  "content": "Tab content...",
  "difficulty": "Intermediate",
  "tuning": "Standard",
  // ... other tab-specific data
}
```

## 🚨 Error Handling

Always handle potential errors when calling the API:

```javascript
try {
    const response = await fetch('http://127.0.0.1:5000/tab?url=...');
    const data = await response.json();
    
    if (response.ok) {
        // Success - use the data
        console.log(data);
    } else {
        // API returned an error
        console.error('API Error:', data.error);
    }
} catch (error) {
    // Network or other error
    console.error('Request failed:', error.message);
}
```

## 🎯 Next Steps

1. **Test the API**: Use `frontend_test.html` to verify everything works
2. **Choose your approach**: Pick the integration method that fits your project
3. **Customize**: Modify the examples to match your app's design and requirements
4. **Add features**: Extend the API with more endpoints as needed

Happy coding! 🎸 