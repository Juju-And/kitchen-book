import flask
from flask import Flask, request
from flask_migrate import Migrate
from sqlalchemy.dialects.postgresql import json

from .models import db, Product, Recipe

app = Flask(__name__)

migrate = Migrate(app, db)

# Please adjust accordingly
POSTGRES = {
    'user': 'postgres',
    'pw': 'coderslab',
    'db': 'kitchenbook',
    'host': 'localhost',
    'port': '5432',
}
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


@app.route('/add-products', methods=['GET', 'POST'])
def addproducts():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            new_record = Product(name=data['name'])
            db.session.add(new_record)
            db.session.commit()
            return flask.Response(status=201)
        else:
            return flask.Response(status=400)

    elif request.method == 'GET':
        records = Product.query.all()
        results = [
            {
                "id": record.product_id,
                "name": record.name,
            } for record in records]

        return {"records": results}


@app.route('/add-recipes', methods=['GET', 'POST'])
def addrecipes():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            new_record = Recipe(name=data['name'])
            db.session.add(new_record)
            db.session.commit()
            return flask.Response(status=201)
        else:
            return flask.Response(status=400)

    elif request.method == 'GET':
        records = Recipe.query.all()
        results = [
            {
                "id": record.recipe_id,
                "name": record.name,
            } for record in records]

        return {"records": results}


@app.route('/recipes/<recipe_id>/ingredients', methods=['GET', 'POST'])
def ingredients(recipe_id):
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            product = Product.query.get(data['product_id'])
            recipe = Recipe.query.get(recipe_id)
            recipe.ingredients.append(product)
            # db.session.add(new_record)
            db.session.commit()
            return flask.Response(status=201)
        else:
            return flask.Response(status=400)
    elif request.method == 'GET':
        recipe = Recipe.query.get(recipe_id)

        ingredients_list = []

        for ingredient in recipe.ingredients:
            ingredients_list.append(ingredient.name)

        results = [
            {
                "ingredients": ingredients_list
            }
        ]
        return {recipe.name: results}




app.config['DEBUG'] = True
if __name__ == '__main__':
    app.run()
