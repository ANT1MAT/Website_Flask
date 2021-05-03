from flask import Flask
from myapp.views import init_blueprints
from myapp.database import db


def create_app():
    # Конфигурация
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOAD_FOLDER'] = 'myapp/uploads'
    SECRET_KEY = 'FgrtGFr43Etr'
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
    db.init_app(app)
    init_blueprints(app)
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
