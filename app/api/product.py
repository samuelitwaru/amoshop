import requests
import json
from . import url_start, attach_token

def get_products():
    url = attach_token(f"{url_start}/products")
    res = requests.get(url)
    return res

def search_product(query_string):
    url = attach_token(f"{url_start}/products?search={query_string}")
    res = requests.get(url)
    return res

def create_product(data):
    url = attach_token(f"{url_start}/products")
    res = requests.post(url, json=data)
    return res

def update_product(product_id, data):
    url = attach_token(f"{url_start}/products/{product_id}")
    res = requests.put(url, json=data)
    return res

def delete_product(product_id):
    url = attach_token(f"{url_start}/products/{product_id}")
    res = requests.delete(url)
    return res