import sys
from PyQt5.QtWidgets import QApplication, QWidget, QStackedWidget
from PyQt5.uic import loadUi
from config import Config


app = QApplication(sys.argv)
from app.uic.login_page import LoginPage

from app.workers import GetProductsWorker


from app.models import create_db, load_products

session = create_db()
get_products_worker = GetProductsWorker()
get_products_worker.onSuccess.connect(load_products)
get_products_worker.start()


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