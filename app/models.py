from app import db
from datetime import date
from flask_login import UserMixin
from sqlalchemy import UniqueConstraint

class Users(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(120), nullable=True)
    username = db.Column(db.String(120), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    email_reminder = db.Column(db.Boolean(), server_default='t') # 'True' by default
    role = db.Column(db.Integer(), server_default='2', nullable=False) # 'Employee' by default

    def __repr__(self):
        return '<User {}>'.format(self.full_name)

class UsersInfo(db.Model):
    __tablename__ = 'users_info'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    date = db.Column(db.Date)
    info = db.Column(db.JSON)

    user = db.relationship('Users', backref='users')
    
    __table_args__ = (UniqueConstraint('user_id', 'date', name='user_date_mc'),)

    def __repr__(self):
            return '<User {}, Date {}>'.format(self.user_id, self.date)