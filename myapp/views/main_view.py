import logging
import os
from flask import Blueprint, request, render_template
from myapp.models.products import Products
from myapp.database import db
from werkzeug.utils import secure_filename

main_blueprint = Blueprint('main_blueprint', __name__,
                           template_folder='../templates/html')


@main_blueprint.route('/', methods=['post', 'get'])
def add_prod_page():
    if request.method == 'POST':
        logging.info('Add data in DB')
        file = request.files['prod_img']
        try:
            add = Products(prod_name=request.form['prod_name'], prod_price=request.form['prod_price'])
            db.session.add(add)
            db.session.commit()
            filename = secure_filename(str(Products.get_id(add)) + str(Products.get_name(add)))
            add_img = db.session.query(Products).get(Products.get_id(add))
            add_img.prod_img = filename
            db.session.add(add_img)
            db.session.commit()
            file.save(os.path.join('myapp/static/uploads', filename))
        except Exception as e:
            db.session.rollback()
            logging.error(f'Error, {e}')
    return render_template('products_add.html')


@main_blueprint.route('/menu/')
def prod_menu():
    menu = Products.query.all()
    return render_template('prod_menu.html', menu=menu)
