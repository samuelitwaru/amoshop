from app import app
from urllib.parse import urlparse, urlencode, parse_qsl, urlunparse


host = "http://127.0.0.1:5000"
host = "http://itwarusamuel.pythonanywhere.com"
pref = "/shop/api/v1.0"
url_start = f"{host}{pref}"


def attach_token(url):
	user = app.user
	if user:
		url_parts = list(urlparse(url))
		params = dict(parse_qsl(url_parts[4]))
		params.update({'token': user.get('token')})
		url_parts[4] = urlencode(params)
		return urlunparse(url_parts)
	else:
		return url


ERRORS = {
    400: "Bad Request",
    401: "Unauthorized",
    402: "Payment Required",
    403: "Forbidden",
    404: "Not Found",
    500: "Internal Server Error",
    501: "Not Implemented",
    503: "Service Unavailable"
}

