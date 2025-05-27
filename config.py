import os
from dotenv import load_dotenv

class Config:
    load_dotenv()
    SQL_USER = os.getenv("SQL_USER", "root")
    SQL_PASSWORD = os.getenv("SQL_PASSWORD", "")
    SQL_DATABASE_NAME = os.getenv("SQL_DATABASE_NAME", "carta_danio_ia")
    SQL_PORT = os.getenv("SQL_PORT", "3306")

    SECRET_KEY = os.getenv('SECRET_KEY')

    SQLALCHEMY_DATABASE_URI = f'mysql+mysqldb://{SQL_USER}:{SQL_PASSWORD}@localhost:{SQL_PORT}/{SQL_DATABASE_NAME}'

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = 'uploads'
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "TU_API_KEY_AQUÍ")
