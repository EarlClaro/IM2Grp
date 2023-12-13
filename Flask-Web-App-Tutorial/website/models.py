from flask_login import UserMixin
from . import db

class User(db.Model, UserMixin):
    userid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

class Category(db.Model):
    categoryID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    userid = db.Column(db.Integer, db.ForeignKey('user.userid'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    user = db.relationship('User', backref='categories', lazy=True)

class Note(db.Model):
    noteID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    userid = db.Column(db.Integer, db.ForeignKey('user.userid'), nullable=False)
    categoryID = db.Column(db.Integer, db.ForeignKey('category.categoryID'))
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.TIMESTAMP, default=db.func.current_timestamp())
    updated_at = db.Column(db.TIMESTAMP, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    user = db.relationship('User', backref='notes', lazy=True)
    category = db.relationship('Category', backref='notes', lazy=True)
