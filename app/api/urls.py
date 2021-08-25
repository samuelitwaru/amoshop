from . import url_start


login = f"{url_start}/users/auth"

user_list = f"{url_start}/users"
user = f"{url_start}/users/<int:id>"
user_auth = f"{url_start}/users/auth"
user_update = f"{url_start}/users/<int:id>/update"

stock_list = f"{url_start}/stock"
stock = f"{url_start}/stock/<int:id>"

sale_list = f"{url_start}/sales"
sale = f"{url_start}/sales/<int:id>"
sale_checkout = f"{url_start}/sales/checkout"

product_list = f"{url_start}/products"
product = f"{url_start}/products/<int:id>"
product_quantity = f"{url_start}/products/<int:id>/quantity"