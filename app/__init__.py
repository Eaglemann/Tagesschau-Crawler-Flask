from flask import Flask
from app.controller_api.controller import controller as controller_bp
from app.explorer_api.explorer import explorer as explorer_bp
from app.db.models import db
from dotenv import load_dotenv
import os
from config import Config
from flask_swagger_ui import get_swaggerui_blueprint


load_dotenv()

def create_app():
    app = Flask(__name__, static_folder='static')

    app.config.from_object(Config)

    # Swagger configuration
    SWAGGER_URL = '/swagger'
    API_URL = '/static/swagger.yaml'

    swagger_ui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': "Future Demand"
        }
    )

    # DB configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("SQLALCHEMY_DATABASE_URI")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    # Register blueprints
    app.register_blueprint(controller_bp, url_prefix="/controller")
    app.register_blueprint(explorer_bp)
    app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL) #Swagger endpoint


    return app
