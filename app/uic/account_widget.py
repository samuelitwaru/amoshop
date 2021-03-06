from PyQt5.QtWidgets import QWidget, QMessageBox
from app import app
from app.forms.user import UpdateUserPasswordForm
from app.workers import SendRequestWorker
from app.uic.uic.account_widget import Ui_Form
from app.api import urls
import requests


class AccountWidget(QWidget):
    def __init__(self, *args):
        super(AccountWidget, self).__init__(*args)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.update_user_password_form = UpdateUserPasswordForm(self.ui.scrollLayout, return_func=self.submit)
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
            self.change_password_worker = SendRequestWorker(urls.user_update.format_map({"id": user_id}), requests.put, json=data)
            self.change_password_worker.started.connect(self.onStarted)
            self.change_password_worker.onSuccessDict.connect(self.onSuccess)
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
