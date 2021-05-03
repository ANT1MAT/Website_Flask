from .main_view import main_blueprint


def init_blueprints(app):
    app.register_blueprint(main_blueprint)
