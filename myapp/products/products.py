import logging
import os
from flask import Blueprint, request, render_template, session
from myapp.models.products import Products
from myapp.database import db
from werkzeug.utils import secure_filename
import datetime


products_blueprint = Blueprint('prod', __name__,
                           template_folder='templates/html',
                           static_folder='static',
                           url_prefix='/product')


@products_blueprint.route('/prod_add', methods=['post', 'get'])
def add_prod_page():
    if request.method == 'POST':
        logging.info('Add data in DB')
        file = request.files['prod_img']
        img_name = secure_filename(str(datetime.datetime.now()))
        try:
            add = Products(name=request.form['name'], price=request.form['price'], img=img_name)
            db.session.add(add)
            file.save(os.path.join('myapp/products/static/uploads', img_name))
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logging.error(f'Error, {e}')
    return render_template('products_add.html')


@products_blueprint.route('/prod_menu/', methods=['post', 'get'])
def prod_menu():
    menu = Products.query.all()
    if request.method == 'POST':
        print(request.form['number'])
        print(request.form['name'])
    return render_template('prod_menu.html', menu=menu)


@products_blueprint.route('/id<prod_id>', methods=['post', 'get'])
def prod_add_in_cart(prod_id):
    product = Products.query.get(prod_id)
    if request.method == 'POST':
        if 'cart' in session:
            x = session['cart']
            x.append({'id': product.id, 'count': request.form['count']})
            print(str(x))
        else:
            x = [{'id': product.id, 'count': request.form['count']}]
        session['cart'] = x
    return render_template('add_prod_in_cart.html', product=product)


@products_blueprint.route('/cart')
def show_cart():
    product = Products.query.all()
    return render_template('cart.html', product=product, cart=session['cart'])
