from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from database import db


class Products(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    price = db.Column(db.String(100), nullable=False)
    img = db.Column(db.String(100))