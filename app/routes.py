from app import app
from flask import render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from flask_sqlalchemy import SQLAlchemy
from app.forms import LoginForm, RegisterForm, WorkPlanForm
from app.forms import LoginForm, RegisterForm, CreateGroupForm, AddToGroupForm, RemoveFromGroupForm, EvaluationForm, WorkPlanForm
from app import db
from app.models import User, Group, Member
import sys


@app.route('/success')
def loginSuccess():
    return render_template('loginSuccess.html')

@app.route('/registerSuccess')
def registerSuccess():
    return render_template('registerSuccess.html')


@app.route('/workplan',methods=['GET', 'POST'])
@login_required
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

@app.route('/evaluation',methods=['GET', 'POST'])
@login_required
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

@app.route('/view_evaluations')
@login_required
def view_evaluation():
    return render_template('viewEvaluations.html')


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
            First_name = form.first_name.data
            Last_name = form.last_name.data
            username = form.username.data
            email = form.email.data
            password = form.password.data
            role = 'user'
            #create user and add to database
            user = User(First_name=First_name, Last_name=Last_name, email=email, username=username, role=role)
            user.set_password(password)
            db.session.add(user)
            member = Member(id=userID, group_id=None, eval_id=None, task_id=None)
            db.session.add(member)
            db.session.commit()
            #will ask user to login to check their credentials
            return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/viewworkplan')
@login_required
def viewworkplan():
    return render_template('view_workplan.html')

@app.route('/create_group', methods=['GET', 'POST'])
@login_required
def create_group():
    if is_admin():
        form = CreateGroupForm()
        if form.validate_on_submit():  
            #get data from the form      
            group = form.groupName.data
            #create a new group and add it to the database
            group = Group(groupName=group)
            db.session.add(group)
            db.session.commit()
            return redirect(url_for('view_groups'))
        return render_template('CreateGroup.html', form=form)
    else:
        return render_template('unauthorized.html')

@app.route('/add_to_group', methods=['GET', 'POST'])
@login_required
def add_to_group():
    if is_admin():
        form = AddToGroupForm()
        if form.validate_on_submit():
            #get the data from the form
            groupName = form.groupName.data
            username = form.username.data
            #get group name and id from database
            group = Group.query.filter_by(groupName=form.groupName.data).first()
            groupID = group.id
            #get the user id
            user = User.query.filter_by(username=username).first()
            userID = user.id
            members = Member.query
            for member in members:
                if user.id == member.id:
                    member.group_id=group.id
            db.session.commit()
            return redirect(url_for('view_groups'))
        return render_template('AddToGroup.html', form=form)
    return render_template('unauthorized.html')

@app.route('/remove_from_group', methods=['GET', 'POST'])
@login_required
def remove_from_group():
    if is_admin():
        form = RemoveFromGroupForm()
        if form.validate_on_submit():
            #get data from form
            groupName = form.groupName.data
            username = form.username.data
            #get group name and id from database
            group = Group.query.filter_by(groupName=form.groupName.data).first()
            groupID = group.id
            #set users groupID to none, this removes the groupID
            user = User.query.filter_by(username=username).first()
            userID = user.id
            members = Member.query
            for member in members:
                if user.id == member.id:
                    member.group_id=None
            db.session.commit()
            return redirect(url_for('view_groups'))
        return render_template('RemoveFromGroup.html', form=form)
    return render_template('unauthorized.html')

@app.route('/view_groups')
@login_required
def view_groups():
    groups = Group.query
    members = Member.query
    user = User.query
    return render_template('ViewGroups.html', groups=groups, members=members, user=user)

def is_admin():
    '''
    Helper function to determine if authenticated user is an admin.
    '''
    if current_user:
        if current_user.role == 'admin':
            return True
        else:
            return False
    else:
        print('User not authenticated.', file=sys.stderr)
