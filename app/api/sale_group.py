import requests
import json
from . import url_start, attach_token


def get_sale_groups():
    url = attach_token(f"{url_start}/sale-groups")
    res = requests.get(url)
    return res