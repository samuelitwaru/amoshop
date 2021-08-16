from PyQt5.QtWidgets import *
from app.res.style import *


class StockPage(QWidget):

    def __init__(self):
        super(StockPage, self).__init__()
        self.initialize_ui()

    def initialize_ui(self):
        v_layout = QVBoxLayout()
        h_layout = QHBoxLayout()
        self.setLayout(v_layout)
        label = QLabel(self, text="Stock", styleSheet=font_24)
        product_list = ProductList()

        # add widgets
        v_layout.addWidget(label, 1)
        v_layout.addLayout(h_layout, 20)

        h_layout.addWidget(product_list)
