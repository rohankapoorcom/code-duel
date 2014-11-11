from duel import app, db
from models import Question, User
from flask import render_template, request, redirect, url_for, session, abort
from flask_login import login_user, logout_user, current_user, login_required


import json

@app.route('/')
def home():
    """Renders the Homepage"""
    return render_template('base.html', user=current_user)

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