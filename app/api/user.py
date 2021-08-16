import requests
import json
from . import url_start, attach_token


def login(data):
    url = f"{url_start}/users/auth"
    res = requests.post(url, json=data)
    return res

def create_user(data):
    url = attach_token(f"{url_start}/users")
    res = requests.post(url, json=data)
    return res


def get_users():
    url = attach_token(f"{url_start}/users")
    res = requests.get(url)
    return res


def delete_user(user_id):
    url = attach_token(f"{url_start}/users/{user_id}")
    res = requests.delete(url)
    return res


def update_user_password(user_id, data):
    url = attach_token(f"{url_start}/users/{user_id}/update")
    res = requests.put(url, json=data)
    return res