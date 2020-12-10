import os
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') if os.environ.get('DATABASE_URL') else 'sqlite:///data.db'
SECRET_KEY = 'super_secret'