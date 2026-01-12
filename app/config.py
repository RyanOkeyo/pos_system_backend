import os 
from datetime import timedelta

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:////tmp/app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False

    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key-change-in-production')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)

    ADMIN_SECURITY_CODE = os.getenv('ADMIN_SECURITY_CODE', 'Jane001')

    CORS_HEADERS = 'Content-Type'

    DEBUG = os.getenv('DEBUG', 'True') == 'True'
    TESTING = False