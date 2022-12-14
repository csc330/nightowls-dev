from flask import Flask, render_template, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, StringField, PasswordField, BooleanField, TextAreaField, RadioField, DateField, DateTimeField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField("Submit")

class RegisterForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    show_password = BooleanField('Show password', id='check')
    submit = SubmitField("Submit")

class WorkPlanForm(FlaskForm):
    groupName = StringField('Group Name: ', validators = [DataRequired()])
    workplan_name = StringField('WorkPlan Name: ', validators = [DataRequired()])
    goal1 = TextAreaField('Goal 1:', validators = [DataRequired()])
    goal2 = TextAreaField('Goal 2:', validators = [DataRequired()])
    goal3 = TextAreaField('Goal 3:', validators = [DataRequired()])
    start_date = DateField('Add Start Date: ', validators = [DataRequired()], format='%Y-%m-%d')
    end_date = DateField('Add End Date: ', validators = [DataRequired()], format='%Y-%m-%d')
    submit = SubmitField("Add a Workplan")


class EvaluationForm(FlaskForm):
    username = StringField("Username: ", validators = [DataRequired()])
    workplan_name = StringField('WorkPlan Name: ', validators = [DataRequired()])
    finished_tasks = StringField("Finished Tasks: ", validators = [DataRequired()])
    add_review = TextAreaField('Further Comments: ', validators = [DataRequired()])
    submit = SubmitField("Submit")


class CreateGroupForm(FlaskForm):
    groupName = StringField('Group Name', validators=[DataRequired()])
    submit = SubmitField("Submit")

class AddToGroupForm(FlaskForm):
    groupName = StringField('Group Name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    submit = SubmitField("Submit")

class RemoveFromGroupForm(FlaskForm):
    groupName = StringField('Group Name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    submit = SubmitField("Submit")
