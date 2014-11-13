from duel import app, db
from duel.models import Question, User
from duel.functions import get_random_question

from flask import render_template, request, redirect, url_for, session, abort
from flask_login import login_user, logout_user, current_user, login_required

import duel

import json

@app.route('/')
def home():
    """Renders the Homepage"""
    return render_template('base.html')

@app.route('/question/<id>/')
def question(id):
    """JSON endpoint to a specific question"""
    question = Question.query.filter_by(id=id).first_or_404()
    return json.dumps(question.to_dict())

@app.route('/register/', methods=['POST'])
def register():
    """Handles user registration for Flask-Login"""
    email = request.form['email']
    registered_user = User.query.filter_by(email=email).first()
    if registered_user:
        return json.dumps({'success': False})
    user = User(email.split('@')[0], request.form['password'], email)
    db.session.add(user)
    db.session.commit()
    return json.dumps({'success': True})
 
@app.route('/login/',methods=['POST'])
def login():
    """Handles user login for Flask-Login"""
    email = request.form['email']
    password = request.form['password']
    registered_user = User.query.filter_by(email=email).first()
    if registered_user is None:
        return json.dumps({'success': False})

    if not registered_user.check_password(password):
        return json.dumps({'success': False})    

    login_user(registered_user, remember=True)
    return json.dumps({'success': True})

@app.route('/logout/')
def logout():
    """Handles user logout for Flask-Logout"""
    logout_user()
    return json.dumps({'success': True})

@app.route('/begin/')
@login_required
def begin():
    """Starts Matchmaking for the duel"""
    duel.user_queue.add_user(current_user)
    if not duel.user_queue.ready_to_play():
        return render_template('wait.html')

    question = get_random_question()
    lines = question.question.split('\n')
    print(question)
    print(lines)
    return render_template('duel.html', lines=lines)
