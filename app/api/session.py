import requests
import json
from . import url_start, attach_token


def create_user_session(user_id, data={}):
    url = attach_token(f"{url_start}/users/{user_id}/session")
    res = requests.post(url, json=data)
    return res


def get_user_session(user_id):
    url = attach_token(f"{url_start}/users/{user_id}/session")
    res = requests.get(url)
    return res


def end_session(session_id):
    url = attach_token(f"{url_start}/sessions/{session_id}")
    res = requests.put(url)
    return res