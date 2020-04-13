from .products import init_routes_products
from .recipes import init_routes_recipes
from .session import init_routes_session


def init_routes(app):
    init_routes_session(app)
    init_routes_recipes(app)
    init_routes_products(app)
