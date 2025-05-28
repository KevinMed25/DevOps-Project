from flask import Flask, jsonify
import os
from dotenv import load_dotenv
from routes import register_routes
from utils.db import init_db
from flask_jwt_extended import JWTManager
from datetime import timedelta
from flask_cors import CORS

init_db()
load_dotenv()
app = Flask(__name__)
CORS(app,  
        origins=["http://localhost:5173", "http://127.0.0.1:5173", "http://localhost:5174", "http://127.0.0.1:5174"],
        allow_headers=["Content-Type", "Authorization"],
        methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        supports_credentials=True
    )

app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
app.config[ 'JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
jwt = JWTManager(app)

app.config['ENV'] = os.getenv('ENV', 'DEVELOPMENT')

register_routes(app)

@app.route('/')
def root():
    """Simple root endpoint that returns API status"""
    return jsonify({
        "status": "API is running",
        "version": "1.0.0",
        "environment": app.config.get('ENV'),
    })
