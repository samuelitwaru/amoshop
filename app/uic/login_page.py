import sys
import time

from PyQt5.QtWidgets import QWidget, QLabel, QMessageBox
from PyQt5.uic import loadUi
from app.views.main_page import MainPage
from app.workers import LoginWorker
from app import app
from app.forms import LoginForm


class LoginPage(QWidget):
    def __init__(self, *args):
        super(LoginPage, self).__init__(*args)
        loadUi('app/uic/uic/login_page.ui', self)
        self.login_form = LoginForm(self.scrollLayout, return_func=self.submit)
        self.login_form.layout_field_widgets()
        self.loginButton.clicked.connect(self.submit)

    def submit(self):
        data = {
            "username": self.login_form.widgets["username"]["input"].text(),
            "password": self.login_form.widgets["password"]["input"].text()
        }
        self.login_form.form_data = data
        if self.login_form.validate_form_data():
            self.worker = LoginWorker(data)
            self.worker.onStarted.connect(self.onLoginStarted)
            self.worker.onSuccess.connect(self.onLoginSuccess)
            self.worker.onError.connect(self.onLoginError)
            self.worker.start()
        self.login_form.show_errors()

    def onLoginStarted(self):
        self.waitLabel.setText("Please wait")

    def onLoginSuccess(self, user):
        app.user = user
        main_page = MainPage(user)
        window = self.parent()
        window.addWidget(main_page)
        window.setCurrentIndex(1)
        self.login_form.clear()
        self.waitLabel.setText("")


    def onLoginError(self, error):
        message = error.get("message")
        reply = QMessageBox.information(self,
                "Information", message)
        if reply == QMessageBox.Ok:
            self.waitLabel.setText("")    
