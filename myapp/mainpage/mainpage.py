from flask import Blueprint, render_template

mainpage_blueprint = Blueprint('mainpage', __name__,
                               template_folder='templates/html')


@mainpage_blueprint.route('/')
def start_page():
    return render_template('mainpage.html')

