from .products import products_blueprint


def products_blueprints(app):
    app.register_blueprint(products_blueprint)
