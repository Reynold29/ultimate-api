from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r'/*': {'origins': '*'}})  # Enable CORS for all routes and origins

# Configure Flask app for longer timeouts
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['PERMANENT_SESSION_LIFETIME'] = 300  # 5 minutes

# Import views
import server.views
