from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine


db = SQLAlchemy()
engine = create_engine("sqlite:///../database/database.db")

class Products(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    prod_name = db.Column(db.String(50), nullable=False)
    prod_price = db.Column(db.String(100), nullable=False)
    prod_img = db.Column(db.String(100))

    def get_id(self):
        return self.id

    def get_name(self):
        return self.prod_name

#это какой-то не реальный костыль, нужно что-то потом придумать
def create_db():
    engine = create_engine("sqlite:///../database/database.db")
    db.metadata.create_all(engine)

