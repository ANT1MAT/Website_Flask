from flask import *
from flask_sqlalchemy import *
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import *

#Конфигурация
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///myapp/database/database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
SECRET_KEY = 'FgrtGFr43Etr'


@app.route('/', methods=['post', 'get'])
def add_prod_page():
    if request.method == 'POST':
        print('Add data in DB')
        try:
            add = Products(prod_name=request.form['prod_name'], prod_price=request.form['prod_price'])
            db.session.add(add)
            db.session.commit()
        except:
            db.session.rollback()
            print('Error')
    return render_template('html/products_add.html')


@app.route('/menu/')
def prod_menu():
    menu = session.query(Products).all()
    return render_template('html/prod_menu.html', menu=menu)


if __name__ == "__main__":
    app.run()
