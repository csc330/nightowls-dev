from app import app
from flask import render_template, redirect, url_for, flash

@app.route('/')
def test():
    return render_template('test.html')
