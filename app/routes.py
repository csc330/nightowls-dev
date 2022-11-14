from app import app
from flask import render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from flask_sqlalchemy import SQLAlchemy
<<<<<<< HEAD
from app.forms import LoginForm, RegisterForm, WorkPlanForm
=======
from app.forms import LoginForm, RegisterForm, CreateGroupForm, AddToGroupForm, RemoveFromGroupForm
>>>>>>> master
from app import db
from app.models import User, Groups
import sys


@app.route('/success')
def loginSuccess():
    return render_template('loginSuccess.html')

@app.route('/registerSuccess')
def registerSuccess():
    return render_template('registerSuccess.html')

<<<<<<< HEAD
@app.route('/workplan',methods=['GET', 'POST'])
def workplan():
    form = WorkPlanForm()
    if form.validate_on_submit():
        Work_plan [form.goal_description.data] = form.WorkPlan.data
        Work_plan [form.project_description.data] = form.WorkPlan.data
        Work_plan [form.project_members.data] = form.WorkPlan.data
        Work_plan [form.current_goals.data] = form.WorkPlan.data
        Work_plan [form.nextphase_goals.data] = form.WorkPlan.data
        form.goal_description.data = ''
        form.project_description.data = ''
        form.project_members.data = ''
        form.current_goals.data = ''
        form.nextphase_goals.data = ' '
        return redirect(url_for('workplan'))
    return render_template('Workplan.html', form=form)
=======
@app.route('/workplan')
def workplan():
    return render_template('Workplan.html')
>>>>>>> master

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
@app.route('/', methods=['GET', 'POST'])
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

<<<<<<< HEAD
@app.route('/viewworkplan')
def viewworkplan():
    return render_template('view_workplan.html')
=======
@app.route('/create_group', methods=['GET', 'POST'])
def create_group():
    form = CreateGroupForm()
    if form.validate_on_submit():        
        group = form.groupName.data
        group = Groups(groupName=group)
        db.session.add(group)
        db.session.commit()
        return redirect(url_for('loginSuccess'))
    return render_template('CreateGroup.html', form=form)

@app.route('/add_to_group', methods=['GET', 'POST'])
def add_to_group():
    form = AddToGroupForm()
    if form.validate_on_submit():
        groupName = form.groupName.data
        username = form.username.data
>>>>>>> master

        group = Groups.query.filter_by(groupName=form.groupName.data).first()
        groupID = group.id

        user = User.query.filter_by(username=username).first()
        user.groupID = groupID
        db.session.commit()
        return render_template('userSuccess.html')
    return render_template('AddToGroup.html', form=form)

@app.route('/remove_from_group', methods=['GET', 'POST'])
def remove_from_group():
    form = RemoveFromGroupForm()
    if form.validate_on_submit():
        groupName = form.groupName.data
        username = form.username.data

        group = Groups.query.filter_by(groupName=form.groupName.data).first()
        groupID = group.id

        user = User.query.filter_by(username=username).first()
        user.groupID = None
        db.session.commit()
        return render_template('userSuccess.html')
    return render_template('AddToGroup.html', form=form)
