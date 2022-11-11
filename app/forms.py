from flask import Flask, render_template, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField("Submit")
    


class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField("Submit")

    
class WorkPlanForm(FlaskForm):
    username = StringField("User's name: ", validators = [DataRequired()])
    goal_description = StringField("Goal Description: ", validators = [DataRequired()])
    submission_time = IntegerField('Time of Submission: ', validators = [DataRequired()])
    project_description = StringField('Project Description', validators = [DataRequired()])
    project_members = StringField('Team Members: ', validators = [DataRequired()])
    current_goals = StringField('Current goals: ', validators = [DataRequired()])
    completed_goals = BooleanField('Completed Goals', validators = [DataRequired()])
    submit = SubmitField("Submit")

class EvaluationForm(FlaskForm):
    username = StringField("User's name: ", validators = [DataRequired()])
    role_description = StringField("Role: ", validators = [DataRequired()])
    submission_history = IntegerField('Submission History: ', validators = [DataRequired()])
    add_review = StringField('Reviews: ', validators = [DataRequired()])
    add_rating = StringField('Ratings: ', validators = [DataRequired()])
    submit = SubmitField("Submit")
