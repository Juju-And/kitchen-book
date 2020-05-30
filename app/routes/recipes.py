import flask
from flask import request, Response, render_template
from flask_login import login_required

from app.models import db, Recipe, Product
from app.schemas import RecipeSchema


def init_routes_recipes(app):
    @app.route("/recipes", defaults={"data_format": "html"}, methods=["GET", "POST"])
    @app.route("/recipes.<data_format>", methods=["GET", "DELETE"])
    @login_required
    def recipes(data_format):

        if request.method == "POST":
            if request.is_json:
                data = request.get_json()
                new_record = Recipe(name=data["name"])
                db.session.add(new_record)
                db.session.commit()
                return flask.Response(status=201)
            else:
                return flask.Response(status=400)
        elif request.method == "GET":
            records = Recipe.query.all()
            if data_format == "json":
                schema = RecipeSchema(only=("recipe_id", "name"), many=True)
                result = schema.dumps(records)
                return Response(
                    response=result, status=200, mimetype="application/json"
                )
            else:
                return render_template("recipes.html", recipes=records, selected_menu='recipes')

    @app.route(
        "/recipes/<recipe_id>",
        defaults={"data_format": "html"},
        methods=["GET", "DELETE"],
    )
    @app.route("/recipes/<recipe_id>.<data_format>", methods=["GET", "DELETE"])
    @login_required
    def handle_recipe(recipe_id, data_format):
        if request.method == "GET":
            record = Recipe.query.get(recipe_id)
            if data_format == "json":
                schema = RecipeSchema(many=True)
                result = schema.dumps(record)
                return Response(
                    response=result, status=200, mimetype="application/json"
                )
            else:
                return render_template("recipe.html", recipe=record)

        elif request.method == "DELETE":
            record = Recipe.query.get(recipe_id)
            db.session.delete(record)
            db.session.commit()
            return flask.Response(status=204)

    @app.route("/recipes/<recipe_id>/ingredients", methods=["GET", "POST"])
    @login_required
    def ingredients(recipe_id):
        if request.method == "POST":
            if request.is_json:
                data = request.get_json()
                product = Product.query.get(data["product_id"])
                recipe = Recipe.query.get(recipe_id)
                recipe.ingredients.append(product)
                db.session.commit()
                return flask.Response(status=201)
            else:
                return flask.Response(status=400)
        elif request.method == "GET":
            recipe = Recipe.query.get(recipe_id)

            ingredients_list = []

            for ingredient in recipe.ingredients:
                ingredients_list.append(ingredient.name)

            results = [{"ingredients": ingredients_list}]
            return {recipe.name: results}
