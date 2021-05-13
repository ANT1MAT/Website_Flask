import logging
import os
from flask import Blueprint, request, render_template, session, flash, redirect
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
    if request.cookies.get('admin') == '1234':
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
        return render_template('products_add.html')
    else:
        return redirect('/')


@products_blueprint.route('/prod_menu/', methods=['post', 'get'])
def prod_menu():
    menu = Products.query.all()
    if request.method == 'POST':
        print(request.form['number'])
        print(request.form['name'])
    return render_template('prod_menu.html', menu=menu)


def stack_items(cart, product):
    for item in cart:
        if item['id'] == product.id:
            item.update(count=float(item['count']) + float(request.form['count']))
            return True


@products_blueprint.route('/id<prod_id>', methods=['post', 'get'])
def prod_add_in_cart(prod_id):
    product = Products.query.get(prod_id)
    if request.method == 'POST':
        if 'cart' in session:
            cart = session['cart']
            if not stack_items(cart, product):
                cart.append({'id': product.id, 'count': request.form['count']})
                session['cart'] = cart
            if len(session['cart']) < 6:
                session['cart'] = cart
                return render_template('add_prod_in_cart.html', product=product)
            else:
                flash('Не возможно добавить товар, корзина переполнена')
        else:
            print('Создание сессии')
            session['cart'] = [{'id': product.id, 'count': request.form['count']}]
    return render_template('add_prod_in_cart.html', product=product)


@products_blueprint.route('/cart', methods=['get'])
def show_cart():
    if not 'cart' in session:
        flash('В вашей корзине ничего нет')
        return render_template('cart.html')
    else:
        product = Products.query.all()
        return render_template('cart.html', product=product, cart=session['cart'])

@products_blueprint.route('/cart', methods=['post'])
def del_item():
    product = Products.query.all()
    cart = session['cart']
    for item in cart:
        if item['id'] == int(request.form['item']):
            cart.remove(item)
    session['cart'] = cart
    return render_template('cart.html', product=product, cart=session['cart'])