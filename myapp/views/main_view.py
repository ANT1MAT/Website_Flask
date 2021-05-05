import logging
import os
from flask import Blueprint, request, render_template
from myapp.models.products import Products
from myapp.models.users import Users, Profiles
from myapp.database import db
from werkzeug.utils import secure_filename
import datetime

main_blueprint = Blueprint('main_blueprint', __name__,
                           template_folder='../templates/html')


@main_blueprint.route('/prod_add', methods=['post', 'get'])
def add_prod_page():
    if request.method == 'POST':
        logging.info('Add data in DB')
        file = request.files['prod_img']
        img_name = secure_filename(str(datetime.datetime.now()))
        try:
            add = Products(name=request.form['name'], price=request.form['price'], img=img_name)
            db.session.add(add)
            db.session.commit()
            file.save(os.path.join('myapp/static/uploads', img_name))
        except Exception as e:
            db.session.rollback()
            logging.error(f'Error, {e}')
    return render_template('products_add.html')


@main_blueprint.route('/prod_menu/')
def prod_menu():
    menu = Products.query.all()
    return render_template('prod_menu.html', menu=menu)
