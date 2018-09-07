from flask import Flask
from config import config_options
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
bootstrap = Bootstrap()
def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_options[config_name])
    bootstrap.init_app(app)
    db.init_app(app)
    #registering main blueprint
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    #initializing the app with the flask extensions
    return app