"""
This module is responsible for creating the Flask application and configuring various components such as:
1. Database (SQLAlchemy)
2. Swagger UI (API Documentation)
3. Blueprints for different controllers and explorers
4. Loading environment variables from a .env file
"""

from flask import Flask
from app.controller_api.controller import controller as controller_bp
from app.explorer_api.explorer import explorer as explorer_bp
from app.db.models import db
from dotenv import load_dotenv
import os
from config import Config
from flask_swagger_ui import get_swaggerui_blueprint

# Load environment variables from the .env file
load_dotenv()

def create_app():
    """
    Factory function to create the Flask application instance.

    Configures the application with settings from:
    1. Environment variables
    2. Swagger UI
    3. SQLAlchemy for database interactions
    4. Blueprints for routing API endpoints

    Returns:
        app: The Flask application instance
    """
    # Initialize the Flask application
    app = Flask(__name__, static_folder='static')

    # Load app configurations from Config class
    app.config.from_object(Config)

    # Swagger UI setup for API documentation
    SWAGGER_URL = '/swagger'  # URL to access Swagger UI
    API_URL = '/static/swagger.yaml'  # Path to Swagger YAML file

    # Initialize Swagger UI Blueprint
    swagger_ui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': "Future Demand"
        }
    )

    # Database configuration using environment variables
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("SQLALCHEMY_DATABASE_URI")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking for performance

    # Initialize the SQLAlchemy database instance
    db.init_app(app)

    # Register application blueprints for routing different parts of the API
    app.register_blueprint(controller_bp, url_prefix="/controller")
    app.register_blueprint(explorer_bp)
    app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)  # Register Swagger UI blueprint

    return app
