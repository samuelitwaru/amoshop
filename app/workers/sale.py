import json
from PyQt5.QtCore import pyqtSignal, QThread
from app import api


class GetSalesWorker(QThread):
    onStarted = pyqtSignal()
    onSuccess = pyqtSignal(list)
    onError = pyqtSignal(dict)

    def __init__(self):
        super().__init__()

    def run(self):
        self.onStarted.emit()
        res = api.get_sales()
        msg = json.loads(res.text)
        if res.status_code == 200:
            self.onSuccess.emit(msg)
        else:
            self.onError.emit(msg)



class CheckoutWorker(QThread):
    onStarted = pyqtSignal()
    onSuccess = pyqtSignal(list)
    onError = pyqtSignal(dict)

    def __init__(self, sales):
        super().__init__()
        self.sales = sales

    def run(self):
        self.onStarted.emit()
        res = api.checkout(self.sales)
        msg = json.loads(res.text)
        if res.status_code == 200:
            self.onSuccess.emit(msg)
        else:
            self.onError.emit(msg)