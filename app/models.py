from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func, TIMESTAMP
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

ingred = db.Table(
    "ingred",
    db.Column("recipe_id", db.Integer, db.ForeignKey("recipe.recipe_id")),
    db.Column("product_id", db.Integer, db.ForeignKey("product.product_id")),
)


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
    # picture = image_attachment('UserPicture') // ToDo
    ingredients = db.relationship(
        "Product", secondary=ingred, backref=db.backref("ingredients", lazy="dynamic")
    )
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)


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
