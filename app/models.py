from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, backref
from sqlalchemy import func, TIMESTAMP

db = SQLAlchemy()

ingred = db.Table('ingred',
                  db.Column('recipe_id', db.Integer, db.ForeignKey('recipe.recipe_id')),
                  db.Column('product_id', db.Integer, db.ForeignKey('product.product_id'))
                  )


class Recipe(db.Model):
    # __tablename__ = 'recipes'

    recipe_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    method = db.Column(db.Text())
    time_created = db.Column(TIMESTAMP, server_default=func.now())
    time_updated = db.Column(TIMESTAMP, server_default=func.now(), onupdate=func.current_timestamp())
    ingredients = db.relationship("Product", secondary=ingred, backref=db.backref('ingredients', lazy='dynamic'))


class Product(db.Model):
    # __tablename__ = 'products'

    product_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=True)


#
class Categories(db.Model):
    # __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    products = db.relationship('Product', backref='category', lazy=True)
