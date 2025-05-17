from flask import Flask, jsonify
import os
from dotenv import load_dotenv
from routes import register_routes
from utils.db import init_db
from flask_jwt_extended import JWTManager
from datetime import timedelta

init_db()
load_dotenv()
app = Flask(__name__)

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
