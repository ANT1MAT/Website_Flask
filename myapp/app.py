import os.path
from flask import Flask
from myapp.products import products_blueprints
from database import db
from myapp.mainpage import mainpage_blueprints

def create_app():
    # Конфигурация
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'FgrtGFr43Etr'
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
    db.init_app(app)

    # Проверка наличия БД
    if os.path.exists('myapp/database/database.db'):
        print('База данных уже существует')
    else:
        db.create_all(app=app)
        print('База данных создана')
    products_blueprints(app)
    mainpage_blueprints(app)
    return app



if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
