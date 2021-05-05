import os.path
from flask import Flask
from myapp.views import init_blueprints
from database import db


def create_app():
    # Конфигурация
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOAD_FOLDER'] = 'myapp/static/uploads'
    SECRET_KEY = 'FgrtGFr43Etr'
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
    db.init_app(app)
    if os.path.exists('myapp/database/database.db'):
        print('Data Base already create')
    else:
        db.create_all(app=app)
        print('Data Base create')
    init_blueprints(app)
    return app



if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
