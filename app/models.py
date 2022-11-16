from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    __tablename__ = 'users'
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

class Workplan(db.Models)
    __tablename__ = 'workplan'
    id = db.Column(db.Integer, foreign_key=True)
    goal_description = db.Column(db.String(64), unique=True)
    project_description = db.Column(db.String(64), primary_key=True, unique=True)
    current_goals = db.Column(db.String(64), unique=True)
    completed_goals = db.Column(db.Boolean, unique=True)

class Evaluation(db.Models)
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
