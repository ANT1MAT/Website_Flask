from flask import Flask
from myapp.views import init_blueprints
from myapp.database import db


def create_app():
    # Конфигурация
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    SECRET_KEY = 'FgrtGFr43Etr'
    db.init_app(app)
    init_blueprints(app)
    return app


if __name__ == "__main__":
    app = create_app()
    app.run()
