import flask
from flask import Flask, request, render_template
from flask_migrate import Migrate
from sqlalchemy.dialects.postgresql import json

from .models import db, Product, Recipe, Categories

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


@app.route('/main', methods=['GET'])
def mainpage():
    if request.method == 'GET':
        return render_template('main.html')


@app.route('/products', methods=['GET', 'POST'])
def products():
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


@app.route('/products/<product_id>', methods=['GET', 'DELETE'])
def handle_product(product_id):
    if request.method == 'GET':
        record = Product.query.get(product_id)
        results = [
            {
                "id": record.product_id,
                "name": record.name,
            }]

        return {"records": results}
    elif request.method == 'DELETE':
        record = Product.query.get(product_id)
        db.session.delete(record)
        db.session.commit()
        return flask.Response(status=204)


@app.route('/products/<product_id>/categories', methods=['GET', 'POST'])
def productcategory(product_id):
    if request.method == 'GET':
        product = Product.query.get(product_id)
        results = [
            {
                "id": product.product_id,
                "name": product.name,
                "category": product.category.name,
            }]

        return {"records": results}

    elif request.method == 'POST':
        product = Product.query.get(product_id)
        if request.is_json:
            data = request.get_json()
            category = Categories.query.get(data['id'])
            category.products.append(product)
            db.session.commit()
            return flask.Response(status=201)
        else:
            return flask.Response(status=400)


@app.route('/recipes', methods=['GET', 'POST'])
def recipes():
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

        # return {"records": results}
        return render_template('recipes.html', recipes=results)


@app.route('/recipes/<recipe_id>', methods=['GET', 'DELETE'])
def handle_recipe(recipe_id):
    if request.method == 'GET':
        record = Recipe.query.get(recipe_id)
        results = [
            {
                "id": record.recipe_id,
                "name": record.name,
            }]

        return {"records": results}

    elif request.method == 'DELETE':
        record = Recipe.query.get(recipe_id)
        db.session.delete(record)
        db.session.commit()
        return flask.Response(status=204)


@app.route('/recipes/<recipe_id>/ingredients', methods=['GET', 'POST'])
def ingredients(recipe_id):
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            product = Product.query.get(data['product_id'])
            recipe = Recipe.query.get(recipe_id)
            recipe.ingredients.append(product)
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
