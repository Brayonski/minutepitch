from flask import render_template,request,flash,redirect,url_for
from . import main
from flask_login import login_required,current_user
from app.models import User
from datetime import datetime
from app import db

@main.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

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

@main.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {
            'author':user, 'body':'test Post#1'
        }
    ]
    return render_template('profile/user_profile.html',posts=posts, user=user)
    '''
    i have used a variant of first() called fist_or_404()
    which works exactly like first() when there are results, and in case there 
    are no results it auto sends a 404 error back
    '''