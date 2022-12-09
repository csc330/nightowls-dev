from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
#import date model to store dates
from datetime import datetime

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    First_name= db.Column(db.String(64))
    Last_name = db.Column(db.String(64))
    username = db.Column(db.String(64), unique=True)
    role = db.Column(db.String(64))
    email = db.Column(db.String(64), unique=True)
    password_hash = db.Column(db.String(256), unique=True)
    member  = db.relationship('Member',backref='member4',lazy=True)
    evaluation  = db.relationship('Evaluation',backref='evaluation',lazy=True)

    def set_password(self, password):
        # Store hashed (encrypted) password in database
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Workplan(db.Models):
    __tablename__ = 'workplan'
    id = db.Column(db.Integer, foreign_key=True)
    goal_description = db.Column(db.String(64), unique=True)
    project_description = db.Column(db.String(64), primary_key=True, unique=True)
    current_goals = db.Column(db.String(64), unique=True)
    completed_goals = db.Column(db.Boolean, unique=True)

class Evaluation(db.Models):
    __tablename__ = 'evalutions'
    id = db.Column(db.Integer, foreign_key=True)
    role_description = db.Column(db.String(64), primary_key=True,  unique=True)
    submission_history =db.Column(db.Integer, unique=True)
    add_review = db.Column(db.String(64), unique=True)
    add_rating = db.Column(db.String(64), unique=True)

# load_user is a function that's used by flask_login to manage the session.
# It simply returns the object associated with the authenticated user.
@login.user_loader
def load_user(id):
    return db.session.query(User).get(int(id))


class Group(db.Model):
    __tablename__ = 'group'
    id = db.Column(db.Integer, primary_key=True)
    groupName = db.Column(db.String(64), unique=True)
    # creating relationship to workplans
    workplans = db.relationship('WorkPlan',backref='workplan',lazy=True)
    member = db.relationship('Member',backref='member1',lazy=True)

class WorkPlan(db.Model):
    __tablename__ = 'workplan'
    id = db.Column(db.Integer, primary_key=True)
    Workplan_name = db.Column(db.String(64))
    goal1 = db.Column(db.String(200))
    goal2 = db.Column(db.String(200))
    goal3 = db.Column(db.String(200))
    start_date = db.Column(db.String(64))
    end_date = db.Column(db.String(64))
    group_id = db.Column(db.Integer, db.ForeignKey(Group.id))

class Evaluation(db.Model):
    __tablename__ = 'evaluation'
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer,db.ForeignKey(User.id), nullable=False)
    rating = db.Column(db.Integer())
    rating1 = db.Column(db.Integer())
    rating2 = db.Column(db.Integer())
    rating3 = db.Column(db.Integer())
    finished_tasks = db.Column(db.String(64), default=False)
    finished_on_time= db.Column(db.String(64), default=False)
    add_review = db.Column(db.String(64))
    date = db.Column(db.DateTime)
    workplan_id = db.Column(db.Integer,db.ForeignKey(WorkPlan.id))
    member= db.relationship('Member',backref='member2',lazy=True)

    
class Member(db.Model):
     __tablename__ = 'member'
     id = db.Column(db.Integer, db.ForeignKey(User.id), primary_key=True)
     group_id = db.Column(db.Integer, db.ForeignKey(Group.id))
     eval_id = db.Column(db.Integer,db.ForeignKey(Evaluation.id))
     workplan_id = db.Column(db.Integer,db.ForeignKey(WorkPlan.id)) 
     
     
     
     
     



