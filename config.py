import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Replace with your MongoDB URI
    MONGO_URI = "your_mongodb_uri_here"
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-please-change'
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'uploads')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///english_app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # 50MB max file size
    # Add other config settings here