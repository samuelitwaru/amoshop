import sys
import time

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QWidget, QLabel, QTableWidgetItem, QHeaderView, QMessageBox
from PyQt5.uic import loadUi
from app import app
from app.forms.user import UpdateUserPasswordForm, CreateUserForm
from app.workers import CreateUserWorker, GetUsersWorker, DeleteUserWorker

from app.res.rcc import user

class UsersWidget(QWidget):
    users = []
    def __init__(self, *args):
        super(UsersWidget, self).__init__(*args)
        loadUi('app/uic/uic/users_widget.ui', self) 

        self.usersTable.itemSelectionChanged.connect(self.show_user)
        self.newUserButton.clicked.connect(self.show_new_user)

        self.usersTable.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.usersTable.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.usersTable.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.usersTable.horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch)

        self.create_user_form = CreateUserForm(self.createUserScroll)
        self.create_user_form.layout_field_widgets()
        self.createUserButton.clicked.connect(self.create_user)
        # self.updateUserButton.clicked.connect(self.update_user)
        self.deleteUserButton.clicked.connect(self.delete_user)
        self.get_users_worker = GetUsersWorker()
        self.get_users_worker.onSuccess.connect(self.load_users_table)
        self.get_users_worker.start()

    def get_user(self, item_id):
        def filter_item(item):
            return item.get("id") == item_id
        for item in list(filter(filter_item, self.users)):
            return item

    def create_user(self):
        data = {
            "name": self.create_user_form.widgets["name"]["input"].text(),
            "email": self.create_user_form.widgets["email"]["input"].text(),
            "telephone": self.create_user_form.widgets["telephone"]["input"].text(),
            "username": self.create_user_form.widgets["username"]["input"].text(),
            "password": self.create_user_form.widgets["password"]["input"].text(),
            "confirm_password": self.create_user_form.widgets["confirm_password"]["input"].text(),
            "roles": list(self.create_user_form.widgets["roles"]["input"].get_data()),
        }
        self.create_user_form.form_data = data
        if self.create_user_form.validate_form_data():
            self.create_user_worker = CreateUserWorker(data)
            self.create_user_worker.onStarted.connect(self.onStarted)
            self.create_user_worker.onSuccess.connect(self.onSuccess)
            self.create_user_worker.onError.connect(self.onError)
            self.create_user_worker.start()

        self.create_user_form.show_errors()

    def delete_user(self):
        currentRow = self.usersTable.currentRow()
        currentCol = 0
        ID = int(self.usersTable.item(currentRow, currentCol).text())
        user = self.get_user(ID)
        profile = user.get("profile")
        msgBox = QMessageBox(QMessageBox.Warning, "Delete User",
                f'Are you sure you want to delete the user "{profile.get("name")}"', QMessageBox.NoButton, self)
        msgBox.addButton("Yes, delete", QMessageBox.AcceptRole)
        msgBox.addButton("Cancel", QMessageBox.RejectRole)
        if msgBox.exec_() == QMessageBox.AcceptRole:
            self.delete_user_worker = DeleteUserWorker(ID)
            self.delete_user_worker.onSuccess.connect(self.load_users_table)
            self.delete_user_worker.start()

    def onStarted(self):
        self.createUserMessageLabel.setText("Please wait ...")

    def onSuccess(self, users):
        self.createUserMessageLabel.setText("")
        self.load_users_table(users)
        self.create_user_form.clear()


    def onError(self, error):
        errors = error.get("message")
        self.create_user_form.errors = errors
        self.create_user_form.show_errors()
        self.createUserMessageLabel.setText("") 

    def update_user(self):
        data = {
            "current_password": self.update_user_password_form.widgets["current_password"]["input"].text(),
            "new_password": self.update_user_password_form.widgets["new_password"]["input"].text(),
            "confirm_password": self.update_user_password_form.widgets["confirm_password"]["input"].text(), 
        }

    def load_users_table(self, users):
        self.users = users
        self.usersTable.setSortingEnabled(False)
        self.usersTable.setRowCount(len(users))
        row = 0
        for user in users:
            profile = user.get("profile")
            name = profile.get("name")
            email = profile.get("email")
            telephone = profile.get("telephone")
            ID = user.get("id")
            self.usersTable.setItem(row, 0, QTableWidgetItem(str(ID)))
            self.usersTable.setItem(row, 1, QTableWidgetItem(name))
            self.usersTable.setItem(row, 2, QTableWidgetItem(email))
            self.usersTable.setItem(row, 3, QTableWidgetItem(telephone))
            row += 1

        self.usersTable.setSortingEnabled(True)

    def show_user(self):
        currentRow = self.usersTable.currentRow()
        currentCol = 0
        ID = int(self.usersTable.item(currentRow, currentCol).text())
        user = self.get_user(ID)
        self.update_user_labels(user)
        self.stackedWidget.setCurrentIndex(1)

    def show_new_user(self):
        self.stackedWidget.setCurrentIndex(0)


    def update_user_labels(self, user):
        profile = user.get("profile")
        self.userIdLabel.setText(str(user.get("id")))
        self.userNameLabel.setText(profile.get("name"))
        self.userEmailLabel.setText(profile.get("email"))
        self.userTelephoneLabel.setText(profile.get("telephone"))
