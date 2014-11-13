"""
Contains the database backed classes: Source, Question
"""

from duel import db, bcrypt
from datetime import datetime
from flask_login import make_secure_token

class Source(db.Model):
    """Represents a source of Questions"""
    __tablename__ = 'sources'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))

    def __init__(self, name):
        """Constructs a Source object"""
        self.name = name

class Question(db.Model):
    """Represents a question/answer pair"""
    __tablename__ = 'questions'

    id = db.Column(db.Integer, primary_key=True)
    source_id = db.Column(db.Integer, db.ForeignKey('sources.id'))
    source = db.relationship(
        'Source',
        backref=db.backref('questions', lazy='dynamic'))
    question = db.Column(db.Text())
    answer = db.Column(db.Text())

    def __init__(self, question, answer, source):
        """Constructs a Question object"""
        self.question = question
        self.answer = answer
        self.source = source

    def to_dict(self):
        """Returns a dictionary representation of this Question"""
        return {
            'question': self.question,
            'answer': self.answer
        }

class User(db.Model):
    """Represents a User for the purpose of authentication and identification"""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120))
    password = db.Column(db.String(60))
    email = db.Column(db.String(120), unique=True, index=True)
    registration_date = db.Column(db.DateTime)
    authentication_token = db.Column(db.String(120))

    def __init__(self, username, password, email):
        """Initializes a new user, using bcrypt to hash their password"""
        self.username = username
        self.password = bcrypt.generate_password_hash(password)
        self.email = email
        self.registration_date = datetime.utcnow()
        self.authentication_token = make_secure_token(self.email, self.password)

    def check_password(self, password):
        """Uses bcrypt to verify user's password"""
        return bcrypt.check_password_hash(self.password, password)

    def is_authenticated(self):
        """If we have a user object, they are authentication"""
        return True
 
    def is_active(self):
        """If we have a user object, they are active"""
        return True
 
    def is_anonymous(self):
        """If we have a user object, they are not anonymous"""
        return False
 
    def get_id(self):
        """Returns the id as a unicode string of the current user"""
        return unicode(self.id)

    def get_auth_token(self):
        """Returns an authentication toekn used to identify this user"""
        return self.authentication_token
 
    def __repr__(self):
        """Allows a text based representation of the current user"""
        return '<User {}>'.format(self.email)
