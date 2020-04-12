from flask import Flask
from flask_migrate import Migrate

from app.models import db

def init_db(app):

    app.config["SECRET_KEY"] = "44cc17091493574f"

    migrate = Migrate(app, db)

    # Please adjust accordingly
    POSTGRES = {
        "user": "postgres",
        "pw": "coderslab",
        "db": "kitchenbook",
        "host": "localhost",
        "port": "5432",
    }
    app.config["SQLALCHEMY_DATABASE_URI"] = (
        "postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s" % POSTGRES
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
