from flask import Flask, jsonify
import os
import logging
import sys # Required for sys.stdout
from pythonjsonlogger import jsonlogger
from dotenv import load_dotenv
from routes import register_routes
from utils.db import init_db
from flask_jwt_extended import JWTManager
from datetime import timedelta
from flask_cors import CORS

log = logging.getLogger() 
log.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
formatter = jsonlogger.JsonFormatter('%(asctime)s %(levelname)s %(module)s %(funcName)s %(lineno)d %(message)s')
handler.setFormatter(formatter)
log.addHandler(handler) 

file_handler = logging.FileHandler('/app/logs/flask_app.log')
file_handler.setFormatter(formatter)
log.addHandler(file_handler) 

werkzeug_logger = logging.getLogger('werkzeug')
werkzeug_logger.addHandler(handler) 
werkzeug_logger.addHandler(file_handler) 
werkzeug_logger.setLevel(logging.DEBUG) 

init_db()
load_dotenv()
app = Flask(__name__)

CORS(app,  
        origins=["http://localhost:5173", "http://127.0.0.1:5173"],
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
    logger = logging.getLogger(__name__) 
    logger.debug("This is a debug log from the root route.")
    logger.info("This is an info log from the root route.")
    logger.warning("This is a warning log from the root route.")
    logger.error("This is an error log from the root route.")
    logger.critical("This is a critical log from the root route.")
    return jsonify({
        "status": "API is running",
        "version": "1.0.0",
        "environment": app.config.get('ENV'),
    })
