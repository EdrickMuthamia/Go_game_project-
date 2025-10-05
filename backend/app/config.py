# app/config.py
from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    # General Flask settings
    SECRET_KEY = os.getenv('SECRET_KEY')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')

    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS', 'False').lower() == 'true'
    
    # JWT settings
    JWT_ACCESS_TOKEN_EXPIRES = os.getenv('JWT_ACCESS_TOKEN_EXPIRES', 'False').lower() == 'true'
    JWT_IDENTITY_CLAIM = os.getenv('JWT_IDENTITY_CLAIM')

    @staticmethod
    def init_app(app):
        """Initialize application-specific configurations"""
        # Ensure instance directory exists for SQLite databases
        if 'sqlite:///' in Config.SQLALCHEMY_DATABASE_URI:
            basedir = os.path.abspath(os.path.dirname(__file__))
            project_root = os.path.dirname(basedir)
            instance_dir = os.path.join(project_root, 'instance')
            if not os.path.exists(instance_dir):
                os.makedirs(instance_dir)