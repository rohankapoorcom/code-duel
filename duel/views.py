from duel import app, db
from duel.models import Question, User
from duel.functions import get_random_question

from flask import render_template, request, redirect, url_for, session, abort, make_response
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
    if 'duel_session' not in request.cookies:
        # Search for a duel_session matching the user_id
        duel_session = duel.duel_sessions.get_session_by_user_id(current_user.id)
        if not duel_session:
            # Perform matchmaking because there's no duel session
            duel.user_queue.add_user(current_user)
            if not duel.user_queue.ready_to_play():
                return render_template('wait.html')

            cur_users = duel.user_queue.get_and_remove_pair()

            # Build duel_session using match made
            duel_session = duel.duel_sessions.add_session(cur_users[0], cur_users[1], get_random_question().id)
            
        # Set cookie with the new duel_session
        response = make_response(redirect(url_for('begin')))
        response.set_cookie('duel_session', duel_session['session_id'])
        return response

    else:
        # Load the dual_session matching the cookie
        duel_session = duel.duel_sessions.get_session_by_id(request.cookies.get('duel_session', 0))
        if not duel_session:
            response = make_response(redirect(url_for('begin')))
            response.set_cookie('duel_session', '', expires=0)
            return response

    question = Question.query.filter_by(id=duel_session['question_id']).first()
    lines = question.question.split('\n')

    return render_template('duel.html', lines=lines)
