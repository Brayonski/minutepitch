import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://yego:pass123@localhost/minutepitch'

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

