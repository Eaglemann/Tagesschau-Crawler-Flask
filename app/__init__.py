from flask import Flask
from app.controller_api.controller import controller as controller_bp
from app.explorer_api.explorer import explorer as explorer_bp
from app.db.models import db
from dotenv import load_dotenv
import os
from config import Config

load_dotenv()

def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    # DB configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("SQLALCHEMY_DATABASE_URI")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    # Register blueprints
    app.register_blueprint(controller_bp, url_prefix="/controller")
    app.register_blueprint(explorer_bp)

    return app
