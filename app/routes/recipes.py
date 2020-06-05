import flask
from flask import request, Response, render_template
from flask_login import login_required
from werkzeug.utils import redirect

from app.forms import AddRecipeFrom
from app.models import db, Recipe, Product
from app.schemas import RecipeSchema

import os


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
                return render_template(
                    "recipes.html", recipes=records, selected_menu="recipes"
                )

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
                print(record.ingredients)
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

    @app.route(
        "/recipes/add", defaults={"data_format": "html"}, methods=["GET", "POST"]
    )
    @app.route("/recipes/add.<data_format>", methods=["GET", "POST"])
    @login_required
    def add_recipes(data_format):
        """
        Add a new recipe
        """

        available_products = db.session.query(Product).all()
        # categories_list = [
        #     (product.id, product.name) for product in available_products
        # ]
        form = AddRecipeFrom(request.form)

        if request.method == "POST":
            # if data_format == "json":
            #     user_data = request.json
            #     schema = CreateRecipeSchema()
            #     result = schema.load(user_data)
            #     db.session.add(result)
            #     db.session.commit()
            # else:
            recipe = Recipe(
                name=form.name.data,
                method=form.method.data,
                preparation_time=form.preparation_time.data,
            )
            if request.files:
                image = request.files["picture"]
                image.save(os.path.join(app.config["IMAGE_UPLOADS"], image.filename))
                recipe.picture = image.filename

            db.session.add(recipe)
            db.session.commit()
            return redirect("/recipes")

        return render_template("addRecipe.html", form=form, selected_menu="recipes")
