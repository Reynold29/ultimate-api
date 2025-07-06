import os
from server import app

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=int(os.environ.get('PORT', 5000)),
        debug=True,
        threaded=True,
        # Increase timeout for development server
        use_reloader=False  # Disable reloader to avoid timeout issues
    )
