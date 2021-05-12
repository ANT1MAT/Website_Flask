# Порядок
import os.path
from flask import Flask
from database import db
from myapp.products import products_blueprints
from myapp.mainpage import mainpage_blueprints


def create_app():
    # Конфигурация
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'FgrtGFr43Etr'
    db.init_app(app)
    # db exists
    if os.path.exists('myapp/database/database.db'):
        # logging ?
        print('Data Base already create')
    else:
        db.create_all(app=app)
        print('Data Base create')
    products_blueprints(app)
    mainpage_blueprints(app)
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
