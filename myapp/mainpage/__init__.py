from .mainpage import mainpage_blueprint


def mainpage_blueprints(app):
    app.register_blueprint(mainpage_blueprint)