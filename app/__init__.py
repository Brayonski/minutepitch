from flask import Flask
from config import config_options
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


db = SQLAlchemy()
bootstrap = Bootstrap()
login_manager = LoginManager()
login_manager.login_vie = 'auth.login'
'''
The auth.login is the function(or endpoint) name for the login views
'''
def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_options[config_name])
    bootstrap.init_app(app)
    db.init_app(app)
    # initializing flask login extension
    login_manager.init_app(app)

    #registering main blueprint
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint,url_prefix = '/authenticate')

    #initializing the app with the flask extensions
    return app