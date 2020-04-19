from marshmallow import Schema, fields, post_load

from app.models import Product, Categories, db


class CategoriesSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    products = fields.List(fields.Nested(lambda: ProductSchema()))


class ProductSchema(Schema):
    product_id = fields.Int()
    name = fields.Str()
    category = fields.Nested(CategoriesSchema, only=["id", "name"])


class CreateProductSchema(Schema):
    product_id = fields.Int()
    name = fields.Str()
    category_name = fields.Str()

    @post_load
    def make_product(self, data, **kwargs):
        category = db.session.query(Categories).filter_by(name=data['category_name']).first()
        if category is not None:
            category_id = category.id
        else:
            new_category = Categories(name=data['category_name'])
            db.session.add(new_category)
            db.session.commit()
            category_id = new_category.id
        del data['category_name']
        return Product(category_id=category_id, **data)


class RecipeSchema(Schema):
    name = fields.Str()
    recipe_id = fields.Int()
    time_created = fields.DateTime()
    time_updated = fields.DateTime()
    method = fields.Str()
    ingredients = fields.List(fields.Nested(lambda: ProductSchema()))
