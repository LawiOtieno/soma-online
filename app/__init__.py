from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config_options
from flask_cors import CORS

db = SQLAlchemy()

def create_app(config_name):
    
    ## Creating a flask application
    app = Flask(__name__)
    CORS(app)

    ## Initialize flask applications
    db.init_app(app)

    ## Creating the app configurations
    app.config.from_object(config_options[config_name])

    ## Registering the blueprint
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    return app