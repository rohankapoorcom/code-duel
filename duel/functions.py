"""
Contains additional functions and classes needed for Code Duel
"""

from duel import login_manager, db
from duel.models import User, Question

import random

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
        if user.id in self.queue:
            return
        self.queue.append(user.id)

    def ready_to_play(self):
        """Check's if there are at least 2 users in the queue"""
        return len(self.queue) >= 2

    def get_and_remove_pair(self):
        """Removes two users from the queue and returns them"""
        user_1 = self.queue.pop(random.randrange(len(self.queue)))
        user_2 = self.queue.pop(random.randrange(len(self.queue)))
        
        return user_1, user_2