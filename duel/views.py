from duel import app, db
from models import Question
from flask import render_template

import json

@app.route('/')
def home():
    return 'Not Implemented'

@app.route('/question/<id>/')
def question(id):
    """JSON endpoint to a specific question"""
    question = Question.query.filter_by(id=id).first_or_404()
    return json.dumps(question.to_dict())