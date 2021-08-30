import sys
from PyQt5.QtWidgets import QApplication, QStackedWidget
from config import Config

app = QApplication(sys.argv)

from app.uic.login_page import LoginPage

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

app.window = window
# login_page.onLoginSuccess({
# 		"roles":["cashier", "admin"]
# 	})