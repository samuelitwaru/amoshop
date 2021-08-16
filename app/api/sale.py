import requests
import json
from . import url_start, attach_token


def get_sales():
    url = attach_token(f"{url_start}/sales")
    res = requests.get(url)
    return res


def checkout(data):
    url = attach_token(f"{url_start}/sales/checkout")
    res = requests.post(url, json=data)
    return res
