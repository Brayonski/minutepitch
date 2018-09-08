from flask import render_template,request,flash,redirect,url_for
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User
from werkzeug.urls import url_parse
from . import auth
from .forms import LoginForm, RegistrationForm
from app import db
from datetime import datetime


##################Registration route section#############
@auth.route('/register', methods = ['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration successfull!')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', title='Register', form=form)


    '''
    first I ensure that the user that invokes this route is
    not logged in. Logic inside if validate_on_submit() creates a 
    new user with the username, email and password provide, writes it to the db
    and then redirects to the login prompt so that the user can ogin


    '''
##################End Registration route section#############





############Log in section##############
'''
The user log in is facilitated by Flask-Login's login_user() function, the value
of the next query string argument is obtained. Flask provides a request variable that
contains all the info that the client sent with the request.
request.args attribute exposes the contents of the query string in a friendly dictionary format
'''

@auth.route('/login', methods=['GET','POST'])
# @login_required
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('invalid username or password')
            return redirect(url_for('auth.login'))
        login_user(user, remember = form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc!= '':
            next_page = url_for('main.index')
        return redirect(next_page)
    return render_template('auth/login.html', title='Sig In', form = form)
    '''
    First step is to load the user from the db,then query 
    the db with the log in username to find the user.
    the result of filetr_by is a query that only
    includes the objects that have a matching username
    since there is only going to be one or zero user results,
    I use first() which will return the user object if it exists,
    or None if it does not.
    first() method is another commonly used way to
    execute a query, when you only need to have
    one result
    Also I call the check_password() method to determine if the password entered in the form matches the hash or not

    '''
############End Log in section##############


@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))

    '''
    offers users the option to log out of the application
    '''