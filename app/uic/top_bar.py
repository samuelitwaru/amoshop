from PyQt5.QtWidgets import QWidget
from app.res.rcc import logo
from app import app
from app.uic.uic.top_bar import Ui_Form


class TopBar(QWidget):
    def __init__(self, *args):
        super(TopBar, self).__init__(*args)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        user = app.user
        if user:
            profile = user.get("profile")
            name = profile.get("name")
            self.ui.userLabel.setText(name)
