from app import app
from flask import render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from flask_sqlalchemy import SQLAlchemy
from app.forms import LoginForm, RegisterForm
from app import db
from app.models import User
import sys

@app.route('/')
def home():
    return render_template('Home.html')

@app.route('/success')
def loginSuccess():
    return render_template('loginSuccess.html')

@app.route('/registerSuccess')
def registerSuccess():
    return render_template('registerSuccess.html')

@app.route('/workplan')
def work():
    return render_template('Workplan.html')

@app.route('/evaluation',methods=['GET', 'POST'])
def evaluation():
    form = EvaluationForm()
    if form.validate_on_submit():
        Evaluation [form.role_description.data] = form.Evaluation.data
        Evaluation [form.submission_history.data] = form.Evaluation.data
        Evaluation [form.add_review.data] = form.Evaluation.data
        Evaluation [form.add_rating.data] = form.Evaluation.data
        form.role_description.data = ''
        form.submission_history.data = ''
        form.add_review.data = ''
        form.add_rating.data = ''
        return redirect(url_for('evaluation'))
    return render_template('Evaluation.html', form=form)

@app.route('/login',methods=['GET', 'POST'])
def login():
    #check if user is already logged in
    #will redirect to homepage
    if current_user.is_authenticated:
        return redirect(url_for('loginSuccess'))
    form = LoginForm()
    if form.validate_on_submit():
        # check DB for user by username
        # have to create user
        user = db.session.query(User).filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            print('Login failed', file=sys.stderr)
            return redirect(url_for('login'))
        # login_user is a flask_login function that starts a session
        login_user(user)
        print('Login successful', file=sys.stderr)
        return redirect(url_for('loginSuccess'))
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        #check if user exists
        user = User.query.filter_by(username=form.username.data).first()
        if user is None:
            #get data from form
            username = form.username.data
            email = form.email.data
            password = form.password.data
            role = 'user'
            #create user and add to database
            user = User(email=email, username=username, role=role)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            #will ask user to login to check their credentials
            return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))




