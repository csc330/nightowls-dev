from flask import Flask, render_template, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, StringField, PasswordField
from wtforms.validators import DataRequired
from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(64), unique=True)
    role = db.Column(db.String(64))
    password_hash = db.Column(db.String(256), unique=True)

    def set_password(self, password):
        # Store hashed (encrypted) password in database
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class LoginForm(FlaskForm):
    username = StringField('username', validators=[DataRequired(), Length(min=4, max=20)])
    password = PasswordField('password', validators=[DataRequired(), Length(min=5, max=10)])
    


class RegisterForm(FlaskForm):
    id = IntegerField('id', validators=[DataRequired(),Length(min=3, max=10) ])
    email = StringField('email', validators=[DataRequired(), Email(message="Invalid Email"), Length(min=6, max=30)])
    username = StringField('username', validators=[DataRequired(), Length(min=4, max=20)])
    password = PasswordField('password', validators=[DataRequired(), Length(min=5, max=10)])
    role = StringField('role', validators=[DataRequired(), Length(min=3, max=20)])


