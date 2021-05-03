import logging
from flask import Blueprint, request, render_template
from myapp.models.products import Products
from myapp.database import db

main_blueprint = Blueprint('main_blueprint', __name__,
                           template_folder='../templates/html')


@main_blueprint.route('/', methods=['post', 'get'])
def add_prod_page():
    if request.method == 'POST':
        logging.info('Add data in DB')
        try:
            add = Products(prod_name=request.form['prod_name'], prod_price=request.form['prod_price'])
            db.session.add(add)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logging.error(f'Error, {e}')
    return render_template('products_add.html')


@main_blueprint.route('/menu/')
def prod_menu():
    menu = Products.query.all()
    return render_template('prod_menu.html', menu=menu)
