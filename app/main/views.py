from flask import render_template
from . import main
@main.route('/')
# @login_required
def index():

    title = 'Welcome to woo'

    return render_template('index.html', title= title)
