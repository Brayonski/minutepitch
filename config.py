import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://yego:pass123@localhost/minutepitch'
    SECRET_KEY=os.environ.get('SECRET_KEY') or '1234'
    pass
class ProdConfig(Config):
    pass
class DevConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://yego:pass123@localhost/minutepitch'
    DEBUG = True

config_options = {
'development':DevConfig,
'production':ProdConfig
}

