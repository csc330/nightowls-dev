from flask import Flask, render_template, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, StringField, PasswordField, BooleanField, TextAreaField
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
    goal_description = TextAreaField("Goal Description: ", validators = [DataRequired()])
    project_description = TextAreaField('Project Description', validators = [DataRequired()])
    project_members = StringField('Team Members: ', validators = [DataRequired()])
    current_goals = StringField('Current goals: ', validators = [DataRequired()])
    nextphase_goals = TextAreaField('Next phasegoals', validators = [DataRequired()])
    submit = SubmitField("Add a Workplan")
