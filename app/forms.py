from flask import Flask, render_template, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, StringField, PasswordField, BooleanField, TextAreaField, RadioField
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
    submit = SubmitField("Submit")

class WorkPlanForm(FlaskForm):
    goal_description = TextAreaField("Goal Description: ", validators = [DataRequired()])
    project_description = TextAreaField('Project Description', validators = [DataRequired()])
    project_members = StringField('Team Members: ', validators = [DataRequired()])
    current_goals = StringField('Current goals: ', validators = [DataRequired()])
    nextphase_goals = TextAreaField('Next phasegoals', validators = [DataRequired()])
    submit = SubmitField("Add a Workplan")


class EvaluationForm(FlaskForm):
    username = StringField("Username: ", validators = [DataRequired()])
    finished_tasks = StringField("Finished Tasks: ", validators = [DataRequired()])
    finished_on_time = StringField('Finished on Time: ', validators=[DataRequired()])
    date = StringField("Today's Date: ", validators=[DataRequired()])
    # add something for question
    add_review = TextAreaField('Further Comments: ', validators = [DataRequired()])
    add_rating = StringField('Overall Rating: ', validators = [DataRequired()])
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
