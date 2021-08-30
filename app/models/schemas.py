from marshmallow import Schema, fields


class ProductSchema(Schema):
	id = fields.Int()
	name = fields.Str()
	brand = fields.Str()
	description = fields.Str()
	barcode = fields.Str()
	quantity = fields.Int()
	buying_price = fields.Int()
	selling_price = fields.Int()
	units = fields.Str()


product_schema = ProductSchema()