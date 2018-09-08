from . import db, login_manager
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash,check_password_hash
from hashlib import md5
from time import time
import jwt


class User(UserMixin, db.Model):
    '''
    UserMixin class that includes generic implementations
    that are appropriate for most user model classes
    '''
    __tablename__ = 'users'
    id =db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), index=True, unique = True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Pitch', backref='author', lazy='dynamic')
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime,default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password_hash,password)
        '''
    with these two methods in place, a user object is now 
    able to do secure password verification
    '''
    def avatar(self,size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)
    '''
    The new avatar() method of the User class returns the URL of the user's avatar image, 
    scaled to the requested size in pixels.For users that don't have an avatar registered, an "identicon" image will be generated
    The verify_reset_password_token() is a static method, which means that it can be invoked directly from the class
    '''

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
        {'reset_password': self.id, 'exp': time() + expires_in},
        app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    ''''
    The get_reset_password_token() function generates a JWT token as a string.

    '''
    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)

        '''
        If the token cannot be validated or is expired, an exception will be raised, and in that case I catch it to prevent the error, and then return None to the caller
        '''
    def __repr__(self):
        return '<User {}>'.format(self.username)
    '''
    Flask-login keeps track of the logged in 
    user by storing its unique identifier in Flask's
    user session.
    ''' 
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

class Pitch(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime,index=True,default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    '''
    Pitch class represent the pitches posted by 
    users. Timestamp is set to default and passsed datetime.utcnow--> function.
    SQLAlchemy will set the field to the value of calling that function
    and not the result of calling it without ()
    The user_id field is initialized as a foreign key to user.id,
    which means that it references an id value from the users table
    '''

    def __repr__(self):
        return '<Pitch{}>'.format(self.body)

        
