from marshmallow import Schema, fields


class ProductSchema(Schema):
    product_id = fields.Int()
    name = fields.Str()
    category_id = fields.Int()


class RecipeSchema(Schema):
    name = fields.Str()
    recipe_id = fields.Int()
    time_created = fields.DateTime()
    time_updated = fields.DateTime()
    method = fields.Str()
    ingredients = fields.List(fields.Nested(lambda: ProductSchema()))
