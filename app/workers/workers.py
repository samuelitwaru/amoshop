from PyQt5.QtCore import pyqtSignal, QThread
from app import api
from app.utils import catch_connection_exception
import requests
import json
from app.api import attach_token



class SendRequestWorker(QThread):
	onStarted = pyqtSignal()
	onSuccessDict = pyqtSignal(dict)
	onSuccessList = pyqtSignal(list)
	onError = pyqtSignal(dict)
	
	def __init__(self, url, request_method, **kwargs):
		super().__init__()
		self.url = attach_token(url)
		self.request_method = request_method
		self.kwargs = kwargs

	@catch_connection_exception
	def run(self):
		self.onStarted.emit()
		res = self.request_method(self.url, **self.kwargs)
		data = json.loads(res.text)
		if res.status_code == 200:
			if isinstance(data, list):
				self.onSuccessList.emit(data)
			elif isinstance(data, dict):
				self.onSuccessDict.emit(data)
		else:
			self.onError.emit(data)