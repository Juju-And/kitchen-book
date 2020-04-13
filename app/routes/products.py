import flask
from flask import request, render_template, Response, flash
from werkzeug.utils import redirect

from app.forms import AddProductFrom
from app.models import Product, db, Categories
from app.schemas import ProductSchema, CreateProductSchema


def init_routes_products(app):
    @app.route("/products", defaults={"data_format": "html"}, methods=["GET", "POST"])
    @app.route("/products.<data_format>", methods=["GET", "POST"])
    def products(data_format):
        records = Product.query.all()
        if request.method == "GET":
            if data_format == "json":
                schema = ProductSchema(many=True)
                result = schema.dumps(records)
                return Response(
                    response=result, status=200, mimetype="application/json"
                )
            else:
                return render_template("products2.html", products=records)

    @app.route("/products/add", defaults={"data_format": "html"}, methods=["GET", "POST"])
    @app.route("/products/add.<data_format>", methods=["GET", "POST"])
    def add_products(data_format):
        """
        Add a new product
        """
        form = AddProductFrom(request.form)

        if request.method == "POST":
            if data_format == "json":
                user_data = request.json
                schema = CreateProductSchema()
                result = schema.load(user_data)
                db.session.add(result)
                db.session.commit()
            else:
                product = Product()
                product.name = form.name.data
                product.category_id = int(form.category.data)
                db.session.add(product)
                db.session.commit()
                return redirect("/products")

        return render_template("addProduct.html", form=form)

    @app.route("/products/<product_id>", methods=["GET", "DELETE"])
    def handle_product(product_id):
        if request.method == "GET":
            record = Product.query.get(product_id)
            results = [{"id": record.product_id, "name": record.name,}]

            return {"records": results}
        elif request.method == "DELETE":
            record = Product.query.get(product_id)
            db.session.delete(record)
            db.session.commit()
            return flask.Response(status=204)

    @app.route("/products/<product_id>/categories", methods=["GET", "POST"])
    def product_category(product_id):
        if request.method == "GET":
            product = Product.query.get(product_id)
            results = [
                {
                    "id": product.product_id,
                    "name": product.name,
                    "category": product.category.name,
                }
            ]

            return {"records": results}

        elif request.method == "POST":
            product = Product.query.get(product_id)
            if request.is_json:
                data = request.get_json()
                category = Categories.query.get(data["id"])
                category.products.append(product)
                db.session.commit()
                return flask.Response(status=201)
            else:
                return flask.Response(status=400)
