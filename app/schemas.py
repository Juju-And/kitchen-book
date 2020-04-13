from marshmallow import Schema, fields


class CategoriesSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    products = fields.List(fields.Nested(lambda: ProductSchema()))


class ProductSchema(Schema):
    product_id = fields.Int()
    name = fields.Str()
    category = fields.Nested(CategoriesSchema, only=["id", "name"])


class RecipeSchema(Schema):
    name = fields.Str()
    recipe_id = fields.Int()
    time_created = fields.DateTime()
    time_updated = fields.DateTime()
    method = fields.Str()
    ingredients = fields.List(fields.Nested(lambda: ProductSchema()))
