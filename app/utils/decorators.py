import functools
import requests
import json

def catch_connection_exception(func):

	@functools.wraps(func)
	def wrapper(*args, **kwargs):
		try:
			func(*args, **kwargs)
		except requests.exceptions.ConnectionError:
			print("Error: Failed to connect")
		except json.decoder.JSONDecodeError as e:
			print("Error: Not a JSON response")
	
	return wrapper