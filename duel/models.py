"""
Contains the database backed classes: Source, Question
"""

from duel import db, bcrypt
import datetime

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
    username = db.Column(db.String(120), unique=True, index=True)
    password = db.Column(db.String(60))
    email = db.Column(db.String(120), unique=True, index=True)
    registration_date = db.Column(db.DateTime)

    def __init__(self, username, password, email):
        self.username = username
        self.password = bcrypt.generate_password_hash(password)
        self.email = email
        self.registration_date = datetime.utcnow()

    def check_password(password):
        return bcrypt.check_password_hash(self.password, password)
