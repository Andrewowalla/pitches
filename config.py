import os

class  Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://andrewowalla:mazla08@localhost/pitchess'

    @staticmethod
    def init_app(app):
        pass

class ProdConfig(Config):
    '''
    Production configuration child class
    '''
    pass

class DevConfig(Config):
    '''
    Development configuration child class
    Args:
        Config: The parent configuration class with General configuration settings
    '''
    DEBUG = True

config_options = {
'development':DevConfig,
'production':ProdConfig
}