import functools
import requests
import json
from PyQt5.QtWidgets import QMessageBox
from app import app


def catch_connection_exception(func):

	@functools.wraps(func)
	def wrapper(*args, **kwargs):
		try:
			func(*args, **kwargs)
		except requests.exceptions.ConnectionError as e:
			print("Error: Failed to connect")
			reply = QMessageBox.information(app.window,
	                "Error", "Error: Failed to connect")
		except json.decoder.JSONDecodeError as e:
			print("Error: Not a JSON response")
	
	return wrapper