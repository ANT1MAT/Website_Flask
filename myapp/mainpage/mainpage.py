from flask import Blueprint, render_template, request, flash, make_response, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash


mainpage_blueprint = Blueprint('mainpage', __name__,
                           template_folder='templates/html')


# Главная страница
@mainpage_blueprint.route('/')
def start_page():
    if request.cookies.get('admin') == '1234':
        return render_template('mainpage.html', admin='admin')
    else:
        return render_template('mainpage.html')


# Осуществления входа в качестве администратора
@mainpage_blueprint.route('/administrator', methods=['post', 'get'])
def admin():
    if request.method == 'POST':
        password = request.form['pass']
        hash = generate_password_hash(password)
        if check_password_hash(hash, 'admin'):
            res = make_response(redirect(url_for('mainpage.start_page')))
            res.set_cookie('admin', '1234', max_age=60 * 7)
            flash('Выполнен вход в качестве администратора')
            return res
        else:
            flash('Неверный пароль')
    return render_template('admin_log.html')

