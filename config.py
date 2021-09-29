import os


class Config:
  SQLALCHEMY_TRACK_MODIFICATIONS=True
  SECRET_KEY = os.environ.get('SECRET_KEY')
  SQLALCHEMY_DATABASE_URI= 'postgresql+psycopg2://access:lawioti@localhost/somaonlinee'
  

class ProdConfig(Config):
  SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL","")
 
class DevConfig(Config):
 
  DEBUG = True



config_options = {
  'production':ProdConfig,
  'development':DevConfig,
  
}
