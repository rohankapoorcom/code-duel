"""
Contains additional functions and classes needed for Code Duel
"""

from duel import login_manager, db, socketio
from duel.models import User, Question

import duel

from flask_socketio import emit

import random
import hashlib

@login_manager.user_loader
def load_user(id):
    """Loads the logged in user from the DB"""
    return User.query.get(int(id))

@login_manager.token_loader
def load_user_by_token(token):
    """Loads the logged in user from the token"""
    return User.query.filter_by(authentication_token=token).first_or_404()

def get_random_question():
    """Pulls a random question from the Database"""
    rand = random.randrange(0, db.session.query(Question).count())
    return db.session.query(Question)[rand]

def get_answer_to_question(question_id):
    """Returns the answer to a specified question_id"""
    return Question.query.filter_by(id=question_id).first_or_404().answer

class UserQueue:
    """
    Represents a queue of users, we randomize the queue when pulling user's
    out from it
    """

    def __init__(self):
        """Constructs a UserQueue object"""
        self.queue = []

    def add_user(self, user):
        """Adds a user to the end of the queue"""
        if not user.id in self.queue:
            self.queue.append(user.id)

    def ready_to_play(self):
        """Check's if there are at least 2 users in the queue"""
        return len(self.queue) >= 2

    def get_and_remove_pair(self):
        """Removes two users from the queue and returns them"""
        user_1 = self.queue.pop(random.randrange(len(self.queue)))
        user_2 = self.queue.pop(random.randrange(len(self.queue)))
        
        return user_1, user_2

class SessionHandler:
    """
    A system that holds a series of sessions containing two users
    and the question they are trying to solve
    """

    def __init__(self):
        """Constructs a SessionHandler object"""
        self.sessions = {}

    def add_session(self, user_1, user_2, question_id):
        """
        Adds a new session to the dictionary of sessions (keyed by session_id)
        """
        session_id = hashlib.md5('{},{},{}'.format(user_1, user_2, question_id)).hexdigest()
        self.sessions[session_id] = {
            'user_1': user_1,
            'user_2': user_2,
            'question_id': question_id,
            'session_id': session_id
        }
        return self.sessions[session_id]

    def get_session_by_id(self, session_id):
        """Returns the session corresponding to the session_id"""
        return self.sessions.get(session_id, None)

    def get_session_by_user_id(self, user_id):
        """Returns the session corresponding to the user_id"""
        for session in self.sessions.values():
            if session['user_1'] == user_id or session['user_2'] == user_id:
                return session
        return None

def compile_code(code):
    code = code.replace('"', '\\"')
    command='python -c "{}"'.format(code)
    contain = duel.docker_client.create_container(image='python', command=command)
    duel.docker_client.start(contain.get('Id'))
    duel.docker_client.wait(contain.get('Id'))
    return duel.docker_client.logs(contain.get('Id')).rstrip()

def grade_submission(submission, answer):
    print('submission: {}'.format(submission))
    print('answer: {}'.format(answer))
    return submission == answer

@socketio.on('submit_code')
def code_submission(data):
    code = data.get('code', '')
    question_id = data.get('question_id')
    user_id = data.get('user_id')
    session_id = data.get('session_id')

    # spawn docker instance
    submission = compile_code(code)
    correctness = grade_submission(
        submission=compile_code(code),
        answer=get_answer_to_question(question_id)
    )
    
    emit('graded_code', {'correct': correctness })
