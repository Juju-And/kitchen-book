from .session import init_routes_session


def init_routes(app):
    init_routes_session(app)