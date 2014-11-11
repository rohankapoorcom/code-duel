"""
Initializes the duel Package - this is especially important
to avoid circular dependencies
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_util_js import FlaskUtilJs 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///..\\data\\test.db'
app.secret_key = 'THIS_IS_A_SECRET'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
fujs = FlaskUtilJs(app)

import os
from parser import QuestionParser

def get_data_path(file_name):
    """Returns the absolute path to the file within the data folder"""

    current_path = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.abspath(os.path.join(current_path, os.pardir, 'data', file_name))
    return data_path

if not os.path.isfile(get_data_path('test.db')):
    db.create_all()
    qp = QuestionParser(get_data_path('problems.txt'), get_data_path('answers.txt'))
    qp.parse(300)

import duel.views

login_manager.login_view = 'login'

import duel.functions