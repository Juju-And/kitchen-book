from flask import request, render_template, Response
from flask_login import login_required
from werkzeug.utils import redirect

from app.forms import AddProductFrom
from app.models import Product, db, Categories
from app.schemas import ProductSchema, CreateProductSchema


def init_routes_products(app):
    @app.route("/products", defaults={"data_format": "html"}, methods=["GET", "POST"])
    @app.route("/products.<data_format>", methods=["GET"])
    @login_required
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

    @app.route(
        "/products/add", defaults={"data_format": "html"}, methods=["GET", "POST"]
    )
    @app.route("/products/add.<data_format>", methods=["GET", "POST"])
    @login_required
    def add_products(data_format):
        """
        Add a new product
        """

        available_categories = db.session.query(Categories).all()
        categories_list = [
            (category.id, category.name) for category in available_categories
        ]
        form = AddProductFrom(request.form)
        form.category.choices = categories_list

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

    @app.route(
        "/products/<product_id>", defaults={"data_format": "html"}, methods=["GET"]
    )
    @app.route("/products/<product_id>.<data_format>", methods=["GET"])
    @login_required
    def handle_product(product_id, data_format):
        record = Product.query.filter_by(product_id=product_id).first()
        if request.method == "GET":
            if data_format == "json":
                schema = ProductSchema()
                result = schema.dumps(record)
                return Response(
                    response=result, status=200, mimetype="application/json"
                )
            else:
                return render_template("product_id.html", product=record)

    @app.route("/products/<product_id>", methods=["DELETE"])
    @login_required
    def delete_product(product_id):
        Product.query.filter_by(product_id=product_id).delete()
        db.session.commit()
