import json
from PyQt5.QtCore import pyqtSignal, QThread
from app import api


class UpdateUserPasswordWorker(QThread):
    onStarted = pyqtSignal()
    onSuccess = pyqtSignal(dict)
    onError = pyqtSignal(dict)
    
    def __init__(self, user_id, data):
        super().__init__()
        self.user_id = user_id
        self.data = data

    def run(self):
        self.onStarted.emit()
        res = api.update_user_password(self.user_id, self.data)
        msg = json.loads(res.text)
        if res.status_code == 200:
            self.onSuccess.emit(msg)
        else:
            self.onError.emit(msg) 


class LoginWorker(QThread):
    onStarted = pyqtSignal()
    onSuccess = pyqtSignal(dict)
    onError = pyqtSignal(dict)

    def __init__(self, data):
        super().__init__()
        self.data = data

    def run(self):
        self.onStarted.emit()
        res = api.login(self.data)
        msg = json.loads(res.text)
        if res.status_code == 200:
            self.onSuccess.emit(msg)
        else:
            self.onError.emit(msg)


class CreateUserWorker(QThread):
    onStarted = pyqtSignal()
    onSuccess = pyqtSignal(list)
    onError = pyqtSignal(dict)

    def __init__(self, data):
        super().__init__()
        self.data = data

    def run(self):
        self.onStarted.emit()
        res = api.create_user(self.data)
        msg = json.loads(res.text)
        if res.status_code == 200:
            self.onSuccess.emit(msg)
        else:
            self.onError.emit(msg)


class GetUsersWorker(QThread):
    onStarted = pyqtSignal()
    onSuccess = pyqtSignal(list)
    onError = pyqtSignal(dict)

    def __init__(self):
        super().__init__()

    def run(self):
        self.onStarted.emit()
        res = api.get_users()
        msg = json.loads(res.text)
        if res.status_code == 200:
            self.onSuccess.emit(msg)
        else:
            self.onError.emit(msg)


class DeleteUserWorker(QThread):
    onStarted = pyqtSignal()
    onSuccess = pyqtSignal(list)
    onError = pyqtSignal(dict)

    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id

    def run(self):
        res = api.delete_user(self.user_id)
        msg = json.loads(res.text)
        if res.status_code == 200:
            self.onSuccess.emit(msg)
        else:
            self.onError.emit(msg)


class UpdateUserWorker(QThread):
    onStarted = pyqtSignal()
    onSuccess = pyqtSignal(list)
    onError = pyqtSignal(dict)

    def __init__(self, user_id, data):
        super().__init__()
        self.user_id = user_id
        self.data = data

    def run(self):
        res = api.update_user(self.user_id, self.data)
        msg = json.loads(res.text)
        if res.status_code == 200:
            self.onSuccess.emit(msg)
        else:
            self.onError.emit(msg)