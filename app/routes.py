from app import app
from flask import render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.forms import LoginForm, RegisterForm
from app import db
from app.forms import User
import sys

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login')
def login():
    #check if user is already logged in
    #will redirect to homepage
    if current_user.is_authenticated:
        return redirect(url_for('/'))
    
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
        return redirect(url_for('view'))
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        #hashed_password = generate_password_hash(form.password.data, method='sha256')
        #new_user = User(id=form.id.data, username=form.username.data, email=form.email.data, password=hashed.password, role=form.role.data)
        #db.session.add(new_user)
        #db.session.commit()
        return 'Successfully registered'

    return render_template('register.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/workplan')
def work():
    return render_template('Workplan.html')

@app.route('/evaluation')
def evaluation():
    return render_template('Evaluation.html')

