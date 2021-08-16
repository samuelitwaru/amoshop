from PyQt5.QtWidgets import *

from app.res.style import *

from app.views.products_table import ProductsTable
from app.uic import CreateProductWidget, UpdateProductWidget


class ProductsPage(QWidget):

	def __init__(self):
	    super(ProductsPage, self).__init__()
	    self.initialize_ui()

	def initialize_ui(self):
		h_layout = QHBoxLayout()
		self.setLayout(h_layout)

		self.products_table = ProductsTable()
		self.create_product_widget = CreateProductWidget()
		self.update_product_widget = UpdateProductWidget()

		# add widgets
		self.stack = QStackedWidget()
		h_layout.addWidget(self.products_table, 3)
		h_layout.addWidget(self.stack, 2)
		self.stack.addWidget(self.create_product_widget)
		self.stack.addWidget(self.update_product_widget)
		
		self.products_table.get_products_worker.start()

	def showUpdateProduct(self, product):
		self.stack.setCurrentIndex(1)
		self.update_product_widget.product = product
		self.update_product_widget.update_product_form.form_data = {
			"name": product.get("name"),
			"description": product.get("description"),
			"barcode": product.get("barcode") or '',
			"buying_price": product.get("buying_price"),
			"selling_price": product.get("selling_price"),
			"units": product.get("units"),
		}
		self.update_product_widget.update_product_form.set_widget_values()

	def showNewProduct(self):
		self.stack.setCurrentIndex(1)

