from . import url_start


user_list = url_start + "/users"
user = url_start + "/users/{id}"
user_auth = url_start + "/users/auth"
user_update = url_start + "/users/{id}/update"

stock_list = url_start + "/stock"
stock = url_start + "/stock/{id}"

sale_list = url_start + "/sales"
sale = url_start + "/sales/{id}"
sale_checkout = url_start + "/sales/checkout"

product_list = url_start + "/products"
product = url_start + "/products/{id}"
product_quantity = url_start + "/products/{id}/quantity"

sale_group_list = url_start + "/sale-groups"
sale_group = url_start + "/sale-groups/{id}"
