import os

class Config:
    # SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://yego:pass123@localhost/minutepitch'
    SECRET_KEY=os.environ.get('SECRET_KEY') or '1234'
    MAIL_SERVER ='smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    
class ProdConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get("HEROKU_POSTGRESQL_COPPER_URL")    
class DevConfig(Config):
    # SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://yego:pass123@localhost/minutepitch'
    DEBUG = True

config_options = {
'development':DevConfig,
'production':ProdConfig
}

heroku addons:create heroku-postgresql -a mymoviedatab
heroku config:set MAIL_PASSWORD=31834310 -a mymoviedatab
heroku config:set MAIL_USERNAME=kibetedgar@gmail.com -a mymoviedatab