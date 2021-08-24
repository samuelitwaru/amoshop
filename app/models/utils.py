from . import session
from . import Product


def load_products(products):
	for product in products:
		p = session.query(Product).get(product.get("id"))
		if not p:
			product = Product(
				id=product.get("id"),
				name=product.get("name"),
				brand=product.get("brand"),
				description=product.get("description"),
				barcode=product.get("barcode"),
				buying_price=product.get("buying_price"),
				selling_price=product.get("selling_price"),
				units=product.get("units"),
			)
			session.add(product)
	session.commit()
