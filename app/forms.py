from flask import Flask, render_template, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, StringField, PasswordField
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
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=20)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=5, max=10)])
    


class RegisterForm(FlaskForm):
    id = IntegerField('id', validators=[InputRequired(),Length(min=3, max=10) ])
    email = StringField('email', validators=[InputRequired(), Email(message="Invalid Email"), Length(min=6, max=30)])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=20)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=5, max=10)])
    role = StringField('role', validators=[InputRequired(), Length(min=3, max=20)])


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
     if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            # compares the password hash in the db and the hash of the password typed in the form
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
               return db.session.query(User).get(int(id))
        return 'invalid username or password'

    return render_template('login.html', form=form)

   


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(id=form.id.data, username=form.username.data, email=form.email.data, password=hashed.password, role=form.role.data)
        db.session.add(new_user)
        db.session.commit()
        return 'Successfully registered'

    return render_template('register.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))



