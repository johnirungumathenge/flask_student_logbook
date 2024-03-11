# models.py

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
# from app import db

db = SQLAlchemy()

class UpdateDetails(db.Model):
    __tablename__ = 'students'

    id = db.Column(db.Integer, primary_key=True)
    work = db.Column(db.Text, nullable=False)
    week = db.Column(db.Text, nullable=False)
    day = db.Column(db.String(100), nullable=False)   
    date = db.Column(db.Date, nullable=True)

    def __repr__(self):
        return f"<Student {self.day} {self.week}>"

class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))
    regno = db.Column(db.String(100))


# db.init_app(app)