import sys
import time
import requests
from PyQt5.QtWidgets import QWidget, QDialog, QLabel, QMessageBox
from PyQt5.uic import loadUi, loadUiType
from app.views.main_page import MainPage
from app.workers import SendRequestWorker, LoginWorker, GetUsersWorker, CreateUserWorker
from app import app
from app.forms import LoginForm, RegisterAsAdminForm
from app.uic.uic import login_page
from app.utils import loadUiClass
from app.uic.uic.login_page import Ui_Form
from app.uic.uic.register_admin import Ui_Form as register_admin_Ui_Form
from app.api import urls



class LoginPage(QWidget):
    def __init__(self, *args):
        super(LoginPage, self).__init__(*args)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.login_form = LoginForm(self.ui.scrollLayout, return_func=self.submit)
        self.login_form.layout_field_widgets()
        self.ui.loginButton.clicked.connect(self.submit)
        self.get_users_worker = GetUsersWorker()
        self.get_users_worker.onSuccess.connect(self.show_register_admin)
        self.get_users_worker.start()

    def submit(self):
        data = {
            "username": self.login_form.widgets["username"]["input"].text(),
            "password": self.login_form.widgets["password"]["input"].text()
        }
        self.login_form.form_data = data
        if self.login_form.validate_form_data():
            self.login_worker = SendRequestWorker(urls.login, requests.post, json=data)
            self.login_worker.onStarted.connect(self.onLoginStarted)
            self.login_worker.onSuccessDict.connect(self.onLoginSuccess)
            self.login_worker.onError.connect(self.onLoginError)
            self.login_worker.start()
        self.login_form.show_errors()

    def onLoginStarted(self):
        self.ui.waitLabel.setText("Please wait")

    def onLoginSuccess(self, user):
        app.user = user
        main_page = MainPage(user)
        window = self.parent()
        window.addWidget(main_page)
        window.setCurrentIndex(1)
        self.login_form.clear()
        self.ui.waitLabel.setText("")

    def onLoginError(self, error):
        message = error.get("message")
        reply = QMessageBox.information(self,
                "Information", message)
        if reply == QMessageBox.Ok:
            self.ui.waitLabel.setText("")  


    def show_register_admin(self, users):
        if len(users) == 0:
            self.register_admin = RegisterAdmin()
            self.register_admin.show()  



class RegisterAdmin(QDialog):
    def __init__(self, *args):
        super(RegisterAdmin, self).__init__(*args)
        self.ui = register_admin_Ui_Form()
        self.ui.setupUi(self)
        self.ui.submitButton.clicked.connect(self.submit)
        self.register_as_admin_form = RegisterAsAdminForm(self.ui.scrollLayout)
        self.register_as_admin_form.layout_field_widgets()


    def submit(self):
        data = {
            "name": self.register_as_admin_form.widgets["name"]["input"].text(),
            "email": self.register_as_admin_form.widgets["email"]["input"].text(),
            "telephone": self.register_as_admin_form.widgets["telephone"]["input"].text(),
            "username": self.register_as_admin_form.widgets["username"]["input"].text(),
            "password": self.register_as_admin_form.widgets["password"]["input"].text(),
            "confirm_password": self.register_as_admin_form.widgets["confirm_password"]["input"].text(),
            "roles": list(self.register_as_admin_form.widgets["roles"]["input"].get_data()),
        }
        self.register_as_admin_form.form_data = data
        if self.register_as_admin_form.validate_form_data():
            self.worker = CreateUserWorker(data)
            self.worker.onStarted.connect(self.onStarted)
            self.worker.onSuccess.connect(self.onSuccess)
            self.worker.onError.connect(self.onError)
            self.worker.start()
        self.register_as_admin_form.show_errors()

    def onStarted(self):
        self.ui.waitLabel.setText("Please wait ...")

    def onSuccess(self):
        self.close()
        reply = QMessageBox.information(self,
                "Information", "Successfully registered as admin.")

    def onError(self, error):
        errors = error.get("message")
        self.register_as_admin_form.errors = errors
        self.register_as_admin_form.show_errors()
        self.ui.waitLabel.setText("") 