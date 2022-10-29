from app import app
from flask import render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
#from app.forms import AddForm, DeleteForm, SearchForm, LoginForm, ChangePasswordForm
#from app import db
#from app.models import User
import sys

@app.route('/')
def test():
    return render_template('test.html')