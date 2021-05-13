from flask import Blueprint,render_template, request, flash, make_response
from werkzeug.security import generate_password_hash, check_password_hash


mainpage_blueprint = Blueprint('mainpage', __name__,
                           template_folder='templates/html')

@mainpage_blueprint.route('/')
def start_page():
    return render_template('mainpage.html')


@mainpage_blueprint.route('/administrator', methods=['post', 'get'])
def admin():
    if request.method == 'POST':
        password = request.form['pass']
        hash = generate_password_hash(password)
        print(hash)
        if check_password_hash(hash, 'admin'):
            res = make_response("Setting a cookie")
            res.set_cookie('admin', '1234', max_age=60 * 2)
            flash('Выполнен вход в качестве администратора')
            return res
        else:
            flash('Неверный пароль')
    print(request.cookies.get('admin'))
    return render_template('admin_log.html')

