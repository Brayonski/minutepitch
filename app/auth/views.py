from flask import render_template,request,flash,redirect,url_for
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User
from werkzeug.urls import url_parse
from . import auth
from .forms import LoginForm

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
        login_user(user(user, remember = form.remember_me.data))
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc!= '':
            next_page = url_for('auth.index')
        return redirect(next_page)
        return redirect(url_for('auth.index'))
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

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

    '''
    offers users the option to log out of the application
    '''