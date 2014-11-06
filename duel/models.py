"""
Contains the database backed classes: Source, Question
"""

from duel import db

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
