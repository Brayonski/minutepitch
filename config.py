import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://yego:pass123@/minutepitch'
    SECRET_KEY=os.environ.get('SECRET_KEY') or '1234'
    MAIL_SERVER ='smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    
class ProdConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
class DevConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://yego:pass123@localhost/minutepitch'
    DEBUG = True

config_options = {
'development':DevConfig,
'production':ProdConfig
}

