from flask import render_template
from . import main
@main.route('/')
# @login_required
def index():

    title = 'Welcome to woo'
    posts = [
    {
        'author': {'username': 'John'},
        'body': 'Beautiful day in Portland!'
    },
    {
        'author': {'username': 'Susan'},
        'body': 'The Avengers movie was so cool!'
    }
    ]

    return render_template('index.html', title= title,posts=posts)
