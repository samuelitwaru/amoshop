from PyQt5.QtCore import pyqtSignal, QThread
from app import api


class Worker(QThread):
	onStarted = pyqtSignal(bool)
	onSuccess = pyqtSignal(bool)
	onError = pyqtSignal(bool)

	def __init__(self, *args, **kwargs):
		pass

	def run(self):
		pass
