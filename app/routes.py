from app import app
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from werkzeug.security import check_password_hash, generate_password_hash
from app.forms import LoginForm, RegisterForm, WorkPlanForm
from app.forms import LoginForm, RegisterForm, CreateGroupForm, AddToGroupForm, RemoveFromGroupForm, EvaluationForm, WorkPlanForm
from app import db
from app.models import User, Group, Member, Evaluation, WorkPlan
import datetime
import sys




@app.route('/success')
def loginSuccess():
    return render_template('loginSuccess.html')


@app.route('/workplan',methods=['GET', 'POST'])
@login_required
def workplan():
    form = WorkPlanForm()
    if is_admin():
        if request.method== 'POST':
            if form.validate_on_submit():
                Workplan_name = form.workplan_name.data
                Goal1 =form.goal1.data
                Goal2= form.goal2.data
                Goal3= form.goal3.data 
                start_date= form.start_date.data
                end_date= form.end_date.data
                groupName = form.groupName.data


                group = db.session.query(Group).filter_by(groupName=form.groupName.data).first()
                if group is None:
                    return render_template('groupNotFound_WP.html')
                else:
                    group_name = group.groupName
                    work_plan = WorkPlan(Workplan_name=Workplan_name, goal1=Goal1, goal2=Goal2, goal3=Goal3, start_date=start_date, end_date=end_date, group_name=group_name)
                    db.session.add(work_plan)
                    db.session.commit()
                    return render_template('WorkPlanSuccess.html')
            else:
                return render_template('unsuccessfulWorkplan.html')
        return render_template('Workplan.html', form=form)
    return render_template('unauthorized.html')



@app.route('/evaluation',methods=['GET', 'POST'])
@login_required
def evaluation():
    form = EvaluationForm()
    if request.method== 'POST':
        if form.validate_on_submit():
            #get data from the form
            user = form.username.data
            workplan_name = form.workplan_name.data
            finished_tasks = form.finished_tasks.data
            rating1 = request.form['question1']
            rating2 = request.form['question2']
            rating3 = request.form['question3']
            date = datetime.datetime.now()
            add_review = form.add_review.data
            add_rating = request.form['overall']

            #get user id to add to evaluation table
            user = db.session.query(User).filter_by(username=form.username.data).first()
            workplan = db.session.query(WorkPlan).filter_by(Workplan_name=form.workplan_name.data).first()
            if user is None:
                return render_template('noUserFound.html')
            elif workplan is None:
                return render_template('noWorkPlan.html')
            else:
                workplanID = workplan.id
                username = user.username
                group = workplan.group_name

                #create evaluation object and add to table
                evaluation = Evaluation(group_name=group, user=username, workplan_id=workplanID, rating=add_rating, rating1=rating1, rating2=rating2, rating3=rating3, finished_tasks=finished_tasks, add_review=add_review, date=date)
                db.session.add(evaluation)
                #commit to database
                db.session.commit()
                return render_template('evalSuccess.html')
        else:
            return render_template('unsuccessfulEval.html', form=form)
    return render_template('Evaluation.html', form=form)
    

@app.route('/view_evaluations')
@login_required
def view_evaluation():
    evaluations = Evaluation.query
    return render_template('viewEvaluations.html', evaluations=evaluations)


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
        password = request.form['password']
        valid_password = check_password_hash(user.password_hash, password)
        if user is None or not valid_password:
            print('Login failed', file=sys.stderr)
            return render_template('unsuccessfulLogin.html', form=form)
        else:
            # login_user is a flask_login function that starts a session
            login_user(user)
            print('Login successful', file=sys.stderr)
            return redirect(url_for('loginSuccess'))
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method== 'POST':
        if form.validate_on_submit():
            #check if user exists
            user = User.query.filter_by(username=form.username.data).first()
            if user is None:
                #get data from form
                First_name = form.first_name.data
                Last_name = form.last_name.data
                username = form.username.data
                email = form.email.data
                password = request.form['password']
                role = 'user'
                #create user and add to database
                user = User(First_name=First_name, Last_name=Last_name, email=email, username=username, role=role)
                user.set_password(password)
                db.session.add(user)
                #get user id and create a new member in database
                user = db.session.query(User).filter_by(username=form.username.data).first()
                userID = user.username
                member = Member(member_id=userID, group_id=None, eval_id=None)
                db.session.add(member)
                db.session.commit()
                #will ask user to login to check their credentials
                return render_template('registerSuccess.html')
        else:
            return render_template('unsuccessfulRegister.html', form=form)
    return render_template('register.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/viewworkplan')
@login_required
def viewworkplan():
    workplan = WorkPlan.query
    member = Member.query
    return render_template('view_workplan.html', workplan=workplan, member=member)

@app.route('/create_group', methods=['GET', 'POST'])
@login_required
def create_group():
    if is_admin():
        form = CreateGroupForm()
        if form.validate_on_submit():  
            group = Group.query.filter_by(groupName=form.groupName.data).first()
            if group is None:
                #get data from the form      
                group = form.groupName.data
                #create a new group and add it to the database
                group = Group(groupName=group)
                db.session.add(group)
                db.session.commit()
                return redirect(url_for('view_groups'))
            else:
                return render_template('groupExists.html', form=form)
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
            #get the user
            user = User.query.filter_by(username=username).first()
            if user is None:
                return render_template('userNotFound_G.html')
            elif group is None:
                return render_template('groupNotFound_G.html')
            else:
                groupID = group.id
                members = Member.query
                for member in members:
                    if user.username == member.member_id:
                        member.group_id=group.groupName
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

            #set users groupID to none, this removes the groupID
            user = User.query.filter_by(username=username).first()
            if user is None:
                return render_template('userNotFound_G.html')
            elif group is None:
                return render_template('groupNotFound_G.html')
            else:
                groupID = group.id
                userID = user.username
                members = Member.query
                for member in members:
                    if user.username == member.member_id:
                        member.group_id=None
                db.session.commit()
                return redirect(url_for('view_groups'))
        return render_template('RemoveFromGroup.html', form=form)
    return render_template('unauthorized.html')

@app.route('/view_groups')
@login_required
def view_groups():
    groups = Group.query
    member = Member.query
    return render_template('ViewGroups.html', groups=groups, member=member)

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

@app.route('/graph')
@login_required
def graph():
    evaluation = Evaluation.query
    rating1 = db.session.query(Evaluation.rating1).filter(Evaluation.user == current_user.username).all()
    rating2 = db.session.query(Evaluation.rating2).filter(Evaluation.user == current_user.username).all()
    rating3 = db.session.query(Evaluation.rating3).filter(Evaluation.user == current_user.username).all()
    overall = db.session.query(Evaluation.rating).filter(Evaluation.user == current_user.username).all()
    
    user = User.query
    rows = db.session.query(User.username).join(Evaluation).filter(Evaluation.user == current_user.username ).count()

    if rows == 0:
        return redirect(url_for('view_evaluation'))
    else:
        xValues = ['Question 1', 'Question 2', 'Question 3']
        print(xValues)

        l1 = [value for value, in rating1]
        yValues1 = sum(l1)/rows
        print(yValues1)

        l2 = [value for value, in rating2]
        yValues2 = sum(l2)/rows 
        print(yValues2)

        l3 = [value for value, in rating3]
        yValues3 = sum(l3)/rows
        print(yValues3)

        l4 = [value for value, in overall]
        yValues4 = sum(l4)
        print(yValues4)

        yValues = []
        yValues.append(yValues1)
        yValues.append(yValues2)
        yValues.append(yValues3)

    return render_template('graph.html', xValues=xValues, yValues=yValues)

@app.route('/graph_admin')
@login_required
def graph_admin():
    evaluation = Evaluation.query
    rating1 = db.session.query(Evaluation.rating1).all()
    rating2 = db.session.query(Evaluation.rating2).all()
    rating3 = db.session.query(Evaluation.rating3).all()
    overall = db.session.query(Evaluation.rating).all()
    group = db.session.query(Group.groupName).all()
    
    user = User.query
    rows = db.session.query(Group.groupName).join(Evaluation).filter(Evaluation.group_name == Evaluation.group_name).count()

    if rows == 0:
        return redirect(url_for('view_evaluation'))
    else:
        xValues = ['Question 1', 'Question 2', 'Question 3']
        print(xValues)

        l1 = [value for value, in rating1]
        yValues1 = sum(l1)/rows
        print(yValues1)

        l2 = [value for value, in rating2]
        yValues2 = sum(l2)/rows 
        print(yValues2)

        l3 = [value for value, in rating3]
        yValues3 = sum(l3)/rows
        print(yValues3)

        l4 = [value for value, in overall]
        yValues4 = sum(l4)
        print(yValues4)

        yValues = []
        yValues.append(yValues1)
        yValues.append(yValues2)
        yValues.append(yValues3)
    
    return render_template('graph.html', xValues=xValues, yValues=yValues)