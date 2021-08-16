import sys
import time

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QWidget
from PyQt5.uic import loadUi

from app.res.rcc import logo
from app import app


class TopBar(QWidget):
    def __init__(self, *args):
        super(TopBar, self).__init__(*args)
        loadUi('app/uic/uic/top_bar.ui', self)
        user = app.user
        if user:
        	profile = user.get("profile")
        	name = profile.get("name")
        	self.userLabel.setText(name)