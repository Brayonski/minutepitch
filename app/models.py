from . import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'
    id =db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), index=True, unique = True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Pitch', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)


