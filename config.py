import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqldb://miusuario:miclave123@localhost:3306/carta_danio_ia'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = 'uploads'
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "TU_API_KEY_AQUÍ")
