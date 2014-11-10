from duel import app, db
from models import Question, User
from flask import render_template, request, flash, redirect, url_for, session, abort
from flask_login import login_user, logout_user, current_user, login_required


import json

@app.route('/')
def home():
    """Renders the Homepage"""
    return 'Welcome to Code Duel'

@app.route('/question/<id>/')
def question(id):
    """JSON endpoint to a specific question"""
    question = Question.query.filter_by(id=id).first_or_404()
    return json.dumps(question.to_dict())

@app.route('/register/' , methods=['GET','POST'])
def register():
    """Handles user registration for Flask-Login"""
    if request.method == 'GET':
        return render_template('register.html')
    user = User(request.form['username'], request.form['password'], request.form['email'])
    db.session.add(user)
    db.session.commit()
    print('User successfully registered')
    return redirect(url_for('login'))
 
@app.route('/login/',methods=['GET','POST'])
def login():
    """Handles user login for Flask-Login"""
    if request.method == 'GET':
        return render_template('login.html')
    username = request.form['username']
    password = request.form['password']
    registered_user = User.query.filter_by(username=username).first()
    if registered_user is None:
        print('Username is invalid' , 'error')
        return redirect(url_for('login'))

    if not registered_user.check_password(password):
        print('password is invalid' , 'error')
        return redirect(url_for('login'))        

    login_user(registered_user)
    print('Logged in successfully')
    return redirect(request.args.get('next') or url_for('home'))