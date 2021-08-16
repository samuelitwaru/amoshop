from PyQt5.QtWidgets import *
from app.uic.sales_widget import SalesWidget

from app.res.style import *


class SalesPage(QWidget):

    def __init__(self):
        super(SalesPage, self).__init__()
        self.initialize_ui()

    def initialize_ui(self):
        v_layout = QVBoxLayout()
        sales_widget = SalesWidget()
        v_layout.addWidget(sales_widget)
