from flask_sqlalchemy import SQLAlchemy
from app import app
# create a new SQLAlchemy object
db = SQLAlchemy(app)


class Products(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    prod_name = db.Column(db.String(50), nullable=True)
    prod_price = db.Column(db.String(100), nullable=True)
