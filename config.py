import os

class Config:
    APP_NAME = "AMO Shop"
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///models/database.db'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    UI_DIR = "app/uic/uic"
    API_SERVER = "http://itwarusamuel.pythonanywhere.com"
