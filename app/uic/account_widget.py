import sys
import time

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QWidget, QLabel, QMessageBox
from PyQt5.uic import loadUi
from app import app
from app.forms.user import UpdateUserPasswordForm
from app.workers import UpdateUserPasswordWorker
from app.uic.uic.account_widget import Ui_Form


class AccountWidget(QWidget):
    def __init__(self, *args):
        super(AccountWidget, self).__init__(*args)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.update_user_password_form = UpdateUserPasswordForm(self.ui.scrollLayout)
        self.update_user_password_form.layout_field_widgets()
        self.ui.submitButton.clicked.connect(self.submit)

    def submit(self):
        data = {
            "current_password": self.update_user_password_form.widgets["current_password"]["input"].text(),
            "new_password": self.update_user_password_form.widgets["new_password"]["input"].text(),
            "confirm_password": self.update_user_password_form.widgets["confirm_password"]["input"].text(), 
        }
        self.update_user_password_form.form_data = data
        if self.update_user_password_form.validate_form_data():
            user_id = app.user.get("id")
            self.change_password_worker = UpdateUserPasswordWorker(user_id, data)
            self.change_password_worker.onStarted.connect(self.onStarted)
            self.change_password_worker.onSuccess.connect(self.onSuccess)
            self.change_password_worker.onError.connect(self.onError)
            self.change_password_worker.start()
        self.update_user_password_form.show_errors()


    def onStarted(self):
        self.ui.progressLabel.setText("Please wait...")

    def onSuccess(self):
        reply = QMessageBox.information(self,
                "Information", "Password was changed successfully.")
        if reply == QMessageBox.Ok:
            self.ui.progressLabel.setText("")
            self.update_user_password_form.clear()

    def onError(self, message):
        errors = message.get("message")
        self.update_user_password_form.errors = errors
        self.update_user_password_form.show_errors()
        self.ui.progressLabel.setText("")
