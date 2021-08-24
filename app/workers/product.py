import json
from PyQt5.QtCore import pyqtSignal, QThread
from app import api


class CreateProductWorker(QThread):
    onStarted = pyqtSignal()
    onSuccess = pyqtSignal(list)
    onError = pyqtSignal(dict)

    def __init__(self, data):
        super().__init__()
        self.data = data

    def run(self):
        self.onStarted.emit()
        res = api.create_product(self.data)
        msg = json.loads(res.text)
        if res.status_code == 200:
            self.onSuccess.emit(msg)
        else:
            self.onError.emit(msg)


class SearchProductWorker(QThread):
    onStarted = pyqtSignal()
    onSuccess = pyqtSignal(list)
    onError = pyqtSignal(dict)

    def __init__(self, query_string):
        super().__init__()
        self.query_string = query_string

    def run(self):
        res = api.search_product(self.query_string)
        msg = json.loads(res.text)
        if res.status_code == 200:
            self.onSuccess.emit(msg)
        else:
            self.onError.emit(msg)



class UpdateProductWorker(QThread):
    onStarted = pyqtSignal()
    onSuccess = pyqtSignal(list)
    onError = pyqtSignal(dict)

    def __init__(self, product, data):
        super().__init__()
        self.product = product
        self.data = data

    def run(self):
        self.onStarted.emit()
        res = api.update_product(self.product.get("id"), self.data)
        msg = json.loads(res.text)
        if res.status_code == 200:
            self.onSuccess.emit(msg)
        else:
            self.onError.emit(msg)


class UpdateProductQuantityWorker(QThread):
    onStarted = pyqtSignal()
    onSuccess = pyqtSignal(list)
    onError = pyqtSignal(dict)

    def __init__(self, product, data):
        super().__init__()
        self.product = product
        self.data = data

    def run(self):
        self.onStarted.emit()
        res = api.update_product_quantity(self.product.get("id"), self.data)
        msg = json.loads(res.text)
        if res.status_code == 200:
            self.onSuccess.emit(msg)
        else:
            self.onError.emit(msg)


class GetProductsWorker(QThread):
    onStarted = pyqtSignal()
    onSuccess = pyqtSignal(list)
    onError = pyqtSignal(dict)

    def __init__(self):
        super().__init__()

    def run(self):
        try:
            res = api.get_products()
            msg = json.loads(res.text)
            if res.status_code == 200:
                self.onSuccess.emit(msg)
            else:
                self.onError.emit(msg)
        except Exception as e:
            print(str(e))
            

class DeleteProductWorker(QThread):
    onStarted = pyqtSignal()
    onSuccess = pyqtSignal(list)
    onError = pyqtSignal(dict)

    def __init__(self, product_id):
        super().__init__()
        self.product_id = product_id

    def run(self):
        res = api.delete_product(self.product_id)
        msg = json.loads(res.text)
        if res.status_code == 200:
            self.onSuccess.emit(msg)
        else:
            self.onError.emit(msg)