import logging
import os
from flask import Blueprint, request, render_template, session, flash, redirect, url_for
from myapp.models.products import Products
from myapp.database import db
from werkzeug.utils import secure_filename
import datetime


products_blueprint = Blueprint('prod', __name__,
                           template_folder='templates/html',
                           static_folder='static',
                           url_prefix='/product')


# Проверяет наличие куки администратора, если проверка проходит успешно,
# предоставляет доступ к странице с добавлением товара/добавляет товар
@products_blueprint.route('/prod_add', methods=['post', 'get'])
def add_prod_page():
    if request.cookies.get('admin') == '1234':
        if request.method == 'POST':
            logging.info('Добавление в БД')
            file = request.files['prod_img']
            img_name = secure_filename(str(datetime.datetime.now()))
            try:
                add = Products(name=request.form['name'], price=request.form['price'], img=img_name)
                db.session.add(add)
                file.save(os.path.join('myapp/products/static/uploads', img_name))
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                logging.error(f'Ошибка, {e}')
            return render_template('products_add.html')
        return render_template('products_add.html')
    else:
        return redirect('/')


# Отображает список добавленных в БД товаров
@products_blueprint.route('/prod_menu/', methods=['get'])
def prod_menu():
    menu = Products.query.all()
    if request.cookies.get('admin') == '1234':
        return render_template('prod_menu.html', menu=menu, admin='admin')
    else:
        return render_template('prod_menu.html', menu=menu)


# Осуществляет удаление товара из базы данных
@products_blueprint.route('/prod_menu/', methods=['post'])
def delete_prod_in_db():
    if request.cookies.get('admin') == '1234':
        id_item = request.form['item']
        obj = Products.query.filter_by(id=id_item).one()
        img_name = obj.img
        os.remove(os.path.join('myapp/products/static/uploads', img_name))
        db.engine.execute("delete from Products where id={}".format(id_item))
    return redirect(url_for('prod.prod_menu'))


# Осуществляет суммирование текущего количества товара и добавляемого
def stack_items(cart, product):
    for item in cart:
        if item['id'] == product.id:
            item.update(count=float(item['count']) + float(request.form['count']))
            return True


# Добавление нового товара в корзину(корзина реализованна через куки сессии)
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


# Показывает содержимое корзины
@products_blueprint.route('/cart', methods=['get'])
def show_cart():
    if 'cart' not in session:
        flash('В вашей корзине ничего нет')
        return render_template('cart.html')
    else:
        product = Products.query.all()
        return render_template('cart.html', product=product, cart=session['cart'])


# Удаляет позицию товара из корзины
@products_blueprint.route('/cart', methods=['post'])
def del_item():
    product = Products.query.all()
    cart = session['cart']
    for item in cart:
        if item['id'] == int(request.form['item']):
            cart.remove(item)
    session['cart'] = cart
    return render_template('cart.html', product=product, cart=session['cart'])
