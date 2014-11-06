from duel import app, db
from models import Question
from flask import render_template

@app.route('/')
def home():
    return 'Not Implemented'

@app.route('/question/<id>/')
def question(id):
    Question.query.filter_by(id=id).one()