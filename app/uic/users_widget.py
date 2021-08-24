import sys
import time

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QWidget, QLabel, QTableWidgetItem, QHeaderView, QMessageBox
from PyQt5.uic import loadUi
from app import app
from app.utils import render_list
from app.forms.user import UpdateUserPasswordForm, CreateUserForm
from app.workers import CreateUserWorker, GetUsersWorker, DeleteUserWorker, UpdateUserWorker
from app.uic.uic.users_widget import Ui_Form
from app.res.rcc import user


class UsersWidget(QWidget):
    users = []
    def __init__(self, *args):
        super(UsersWidget, self).__init__(*args)
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.ui.usersTable.itemSelectionChanged.connect(self.show_user)
        self.ui.newUserButton.clicked.connect(self.show_new_user)

        self.ui.usersTable.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.ui.usersTable.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.ui.usersTable.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.ui.usersTable.horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch)

        self.create_user_form = CreateUserForm(self.ui.createUserScroll)
        self.create_user_form.layout_field_widgets()
        self.ui.createUserButton.clicked.connect(self.create_user)
        # self.updateUserButton.clicked.connect(self.update_user)
        self.ui.deleteUserButton.clicked.connect(self.delete_user)
        self.ui.toggleUserStateButton.clicked.connect(self.toggle_user_state)
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
        currentRow = self.ui.usersTable.currentRow()
        currentCol = 0
        ID = int(self.ui.usersTable.item(currentRow, currentCol).text())
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

    def toggle_user_state(self):
        currentRow = self.ui.usersTable.currentRow()
        currentCol = 0
        ID = int(self.ui.usersTable.item(currentRow, currentCol).text())
        user = self.get_user(ID)
        profile = user.get("profile")
        is_active = user.get("is_active")
        if is_active: 
            action = "Deactivate"
        else:
            action = "Activate"
        msgBox = QMessageBox(QMessageBox.Warning, f"{action} User",
                f'Are you sure you want to {action} the user "{profile.get("name")}"', QMessageBox.NoButton, self)
        msgBox.addButton(f"Yes, {action}", QMessageBox.AcceptRole)
        msgBox.addButton("Cancel", QMessageBox.RejectRole)
        if msgBox.exec_() == QMessageBox.AcceptRole:
            data = {"is_active": not user.get("is_active")}
            self.update_user_worker = UpdateUserWorker(ID, data)
            self.update_user_worker.onSuccess.connect(self.onUpdateUserSuccess)
            self.update_user_worker.start()

    def onStarted(self):
        self.ui.createUserMessageLabel.setText("Please wait ...")

    def onSuccess(self, users):
        self.ui.createUserMessageLabel.setText("")
        self.load_users_table(users)
        self.create_user_form.clear()

    def onUpdateUserSuccess(self, users):
        self.load_users_table(users)
        self.show_user()

    def onError(self, error):
        errors = error.get("message")
        self.create_user_form.errors = errors
        self.create_user_form.show_errors()
        self.ui.createUserMessageLabel.setText("") 

    def update_user(self):
        data = {
            "current_password": self.update_user_password_form.widgets["current_password"]["input"].text(),
            "new_password": self.update_user_password_form.widgets["new_password"]["input"].text(),
            "confirm_password": self.update_user_password_form.widgets["confirm_password"]["input"].text(), 
        }

    def load_users_table(self, users):
        self.users = users
        self.ui.usersTable.setSortingEnabled(False)
        self.ui.usersTable.setRowCount(len(users))
        row = 0
        for user in users:
            profile = user.get("profile")
            name = profile.get("name")
            email = profile.get("email")
            telephone = profile.get("telephone")
            ID = user.get("id")
            self.ui.usersTable.setItem(row, 0, QTableWidgetItem(str(ID)))
            self.ui.usersTable.setItem(row, 1, QTableWidgetItem(name))
            self.ui.usersTable.setItem(row, 2, QTableWidgetItem(email))
            self.ui.usersTable.setItem(row, 3, QTableWidgetItem(telephone))
            row += 1

        self.ui.usersTable.setSortingEnabled(True)

    def show_user(self):
        currentRow = self.ui.usersTable.currentRow()
        currentCol = 0
        ID = int(self.ui.usersTable.item(currentRow, currentCol).text())
        user = self.get_user(ID)
        self.update_user_labels(user)
        self.ui.stackedWidget.setCurrentIndex(1)

    def show_new_user(self):
        self.ui.stackedWidget.setCurrentIndex(0)

    def update_user_labels(self, user):
        profile = user.get("profile")
        is_active = user.get("is_active")
        self.ui.userIdLabel.setText(str(user.get("id")))
        self.ui.userNameLabel.setText(profile.get("name"))
        self.ui.userEmailLabel.setText(profile.get("email"))
        self.ui.userTelephoneLabel.setText(profile.get("telephone"))
        self.ui.userRolesLabel.setText(render_list(user.get("roles")))
        if is_active:
            self.ui.toggleUserStateButton.setText("Deactivate")
        else:
            self.ui.toggleUserStateButton.setText("Activate")

