import sys
from PyQt5.QtWidgets import QApplication, QWidget, QStackedWidget
from PyQt5.uic import loadUi
from config import Config
import requests

app = QApplication(sys.argv)
from app.uic.login_page import LoginPage
from app.uic.register_admin import RegisterAdmin

from app.workers import GetProductsWorker, SendRequestWorker


from app.models import create_db


session = create_db()


app.user = None

# pages
login_page = LoginPage()


window = QStackedWidget()
window.addWidget(login_page)
window.show()
window.setWindowTitle(Config.APP_NAME)
window.setGeometry(10, 10, 800, 700)

# login_page.onLoginSuccess({
# 		"roles":["cashier", "admin"]
# 	})