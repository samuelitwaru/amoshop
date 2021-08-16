import json
from PyQt5.QtCore import pyqtSignal, QThread
from app import api


class GetSaleGroupsWorker(QThread):
    onStarted = pyqtSignal()
    onSuccess = pyqtSignal(list)
    onError = pyqtSignal(dict)

    def __init__(self):
        super().__init__()

    def run(self):
        self.onStarted.emit()
        res = api.get_sale_groups()
        msg = json.loads(res.text)
        if res.status_code == 200:
            self.onSuccess.emit(msg)
        else:
            self.onError.emit(msg)