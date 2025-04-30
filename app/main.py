from flask import Flask, jsonify
import os
from dotenv import load_dotenv
from app.routes import register_routes
from app.utils.db import init_db
from app.models import Driver

init_db()
load_dotenv()

app = Flask(__name__)
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
