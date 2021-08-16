import json
from PyQt5.QtCore import pyqtSignal, QThread
from app import api


class CreateUserSessionWorker(QThread):
    onStarted = pyqtSignal()
    onSuccess = pyqtSignal(dict)
    onError = pyqtSignal(dict)

    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id

    def run(self):
        self.onStarted.emit()
        res = api.create_user_session(self.user_id)
        msg = json.loads(res.text)
        if res.status_code == 200:
            self.onSuccess.emit(msg)
        else:
            self.onError.emit(msg)


class GetUserSessionWorker(QThread):
    onStarted = pyqtSignal()
    onSuccess = pyqtSignal(dict)
    onError = pyqtSignal(dict)

    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id 

    def run(self):
        self.onStarted.emit()
        res = api.get_user_session(self.user_id)
        msg = json.loads(res.text)
        if res.status_code == 200:
            self.onSuccess.emit(msg)
        else:
            self.onError.emit(msg)

class EndSessionWorker(QThread):
    onStarted = pyqtSignal()
    onSuccess = pyqtSignal(dict)
    onError = pyqtSignal(dict)

    def __init__(self, session_id):
        super().__init__()
        self.session_id = session_id 

    def run(self):
        self.onStarted.emit()
        res = api.end_session(self.session_id)
        msg = json.loads(res.text)
        if res.status_code == 200:
            self.onSuccess.emit(msg)
        else:
            self.onError.emit(msg)