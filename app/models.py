from . import db, login_manager
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash,check_password_hash
from hashlib import md5
from time import time
import jwt
from app import create_app

followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('users.id'))
)
'''
auxiliary table that has no data other than the foreign keys, I created it without an associated model class.
'''

class User(UserMixin, db.Model):
    '''
    UserMixin class that includes generic implementations
    that are appropriate for most user model classes
    '''
    __tablename__ = 'users'
    id =db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), index=True, unique = True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(130))
    pitch = db.relationship('Pitch', backref='author', lazy='dynamic')
    about_me = db.Column(db.String(150))
    last_seen = db.Column(db.DateTime,default=datetime.utcnow)
    followed = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')
    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        return self.followed.filter(
            followers.c.followed_id == user.id).count() > 0
    
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

    def followed_posts(self):
        followed = Pitch.query.join(
            followers, (followers.c.followed_id == Pitch.user_id)).filter(
                followers.c.follower_id == self.id)
        own = Pitch.query.filter_by(user_id=self.id)
        return followed.union(own).order_by(Pitch.timestamp.desc())

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
    __tablename__= 'pitches'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime,index=True,default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    '''
    Pitch class represent the pitches Pitched by 
    users. Timestamp is set to default and passsed datetime.utcnow--> function.
    SQLAlchemy will set the field to the value of calling that function
    and not the result of calling it without ()
    The user_id field is initialized as a foreign key to user.id,
    which means that it references an id value from the users table
    '''

    def __repr__(self):
        return '<Pitch{}>'.format(self.body)

        
