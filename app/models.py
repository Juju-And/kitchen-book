from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func, TIMESTAMP
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.declarative import declarative_base
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy_imageattach.entity import Image, image_attachment

Base = declarative_base()

db = SQLAlchemy()


class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey("recipe.recipe_id"))
    product_id = db.Column(db.Integer, db.ForeignKey("product.product_id"))
    recipe = db.relationship("Recipe", foreign_keys="Ingredient.recipe_id")
    product = db.relationship("Product", foreign_keys="Ingredient.product_id")


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=True, default="default.jpg")
    password_hash = db.Column(db.String(), nullable=False)
    recipes = db.relationship("Recipe", backref="author", lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Recipe(db.Model):
    # __tablename__ = 'recipes'

    recipe_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    method = db.Column(db.Text())
    time_created = db.Column(TIMESTAMP, server_default=func.now())
    time_updated = db.Column(
        TIMESTAMP, server_default=func.now(), onupdate=func.current_timestamp()
    )
    preparation_time = db.Column(db.String())
    # picture = image_attachment("FoodPicture")
    picture = db.Column(db.String())
    ingredients_relationship = db.relationship(
        "Product",
        secondary="ingredient",
        backref=db.backref("ingredients", lazy="dynamic"),
    )
    ingredients = association_proxy(
        "ingredients_relationship", "name", creator=lambda name: Product(name=name),
    )
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)


# class FoodPicture(Base, Image):
#     """Food picture model."""
#
#     recipe_id = db.Column(db.Integer, db.ForeignKey("recipe.recipe_id"), primary_key=True)
#     recipe = db.relationship("Recipe")
#     __tablename__ = "food_picture"


class Product(db.Model):
    # __tablename__ = 'products'

    product_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=True)


class Categories(db.Model):
    # __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    products = db.relationship("Product", backref="category", lazy=True)
