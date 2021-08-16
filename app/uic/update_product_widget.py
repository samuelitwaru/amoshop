import sys
import time

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt5.uic import loadUi
from PyQt5.QtCore import pyqtSignal, QThread

from app.utils import clear_layout
from app.forms import UpdateProductForm
from app.workers import UpdateProductWorker


class UpdateProductWidget(QWidget):
    product = None

    def __init__(self, *args):
        super(UpdateProductWidget, self).__init__(*args)
        loadUi('app/uic/uic/update_product_widget.ui', self)
        self.update_product_form = UpdateProductForm(box_layout=self.scrollLayout)
        self.update_product_form.layout_field_widgets()

    @pyqtSlot()
    def on_newProductButton_clicked(self):
        self.parent().setCurrentIndex(0)

    @pyqtSlot()
    def on_submitButton_clicked(self):
    	# get data
        data = {
            "name": self.update_product_form.widgets["name"]["input"].text(),
            "brand": self.update_product_form.widgets["brand"]["input"].text(),
            "description": self.update_product_form.widgets["description"]["input"].toPlainText(),
            "barcode": self.update_product_form.widgets["barcode"]["input"].text(),
            "buying_price": self.update_product_form.widgets["buying_price"]["input"].text(),
            "selling_price": self.update_product_form.widgets["selling_price"]["input"].text(), 
            "units": self.update_product_form.widgets["units"]["input"].text(), 
        }
        self.update_product_form.form_data = data
        if self.update_product_form.validate_form_data():
            self.worker = UpdateProductWorker(self.product, data)
            self.worker.onStarted.connect(self.onStarted)
            self.worker.onSuccess.connect(self.onSuccess)
            self.worker.onError.connect(self.onUpdateProductError)
            self.worker.start()
        self.update_product_form.show_errors()


    def setForm(self, product):
    	clear_layout(self.scrollLayout)
    	self.product = product
    	self.update_product_form = UpdateProductForm(product, box_layout=self.scrollLayout)
    	self.update_product_form.layout_field_widgets()

    def onStarted(self):
    	self.progressLabel.setText("Please wait...")

    def onSuccess(self, products):
        self.parent().parent().products_table.onDataFetched(products)
        self.progressLabel.setText("")

    def onUpdateProductError(self, message):
        errors = message.get("message")
        self.update_product_form.errors = errors
        self.update_product_form.show_errors()
        self.progressLabel.setText("")

