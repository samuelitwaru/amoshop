from PyQt5.QtWidgets import QWidget, QDialog

from app import app
from app.uic.uic.register_admin import Ui_Form


class RegisterAdmin(QDialog):
    def __init__(self, *args):
        super(RegisterAdmin, self).__init__(*args)
        self.ui = Ui_Form()
        self.ui.setupUi(self)