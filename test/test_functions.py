"""Unit tests for the functions module"""

from duel.functions import UserQueue, SessionHandler, compile_code, grade_submission

from nose import with_setup

import docker
import mock

docker_client = docker.Client(base_url='tcp://alphadev:2375')

queue = None
user1 = None
user2 = None

handler = None
question_id = None

"""Setup/Teardown Functions"""

def setup_users():
    global queue, user1, user2
    queue = UserQueue()
    user1 = mock.Mock()
    user1.id = 7
    user2 = mock.Mock()
    user2.id = 5

def setup_sessions():
    global handler, question_id
    setup_users()
    handler = SessionHandler()
    question_id = 9

def teardown():
    pass

"""Tests for the UserQueue class"""

@with_setup(setup_users, teardown)
def test_user_queue_no_users():
    assert not queue.ready_to_play()

@with_setup(setup_users, teardown)
def test_user_queue_single_user():
    queue.add_user(user1)
    assert queue.queue[0] == user1.id
    assert not queue.ready_to_play()

@with_setup(setup_users, teardown)
def test_user_queue_two_users():
    queue.add_user(user1)
    assert queue.queue[0] == user1.id
    assert not queue.ready_to_play()
    queue.add_user(user2)
    assert queue.queue[1] == user2.id
    assert queue.ready_to_play()

@with_setup(setup_users, teardown)
def test_user_queue_duplicate_users():
    queue.add_user(user1)
    assert queue.queue[0] == user1.id
    assert not queue.ready_to_play()
    queue.add_user(user1)
    assert queue.queue[0] == user1.id
    assert len(queue.queue) == 1
    assert not queue.ready_to_play()

"""Tests for the SessionHandler class"""

@with_setup(setup_sessions, teardown)
def test_session_handler_add_session():
    session = handler.add_session(user1.id, user2.id, question_id)
    assert session['user_1_id'] == user1.id
    assert session['user_2_id'] == user2.id
    assert session['question_id'] == question_id

@with_setup(setup_sessions, teardown)
def test_session_handler_get_session_by_id():
    session = handler.add_session(user1.id, user2.id, question_id)
    assert handler.get_session_by_id(session['session_id']) == session

@with_setup(setup_sessions, teardown)
def test_session_handler_get_session_by_user_id():
    session = handler.add_session(user1.id, user2.id, question_id)
    assert handler.get_session_by_user_id(session['user_1_id']) == session
    assert handler.get_session_by_user_id(session['user_2_id']) == session
    assert handler.get_session_by_user_id(8) == None

"""Tests for the compile_code function"""

def test_compile_code_no_code():
    assert compile_code(docker_client, '') == ''

def test_compile_code_single_quotes():
    code = "print('Hello, World')"
    assert compile_code(docker_client, code) == 'Hello, World'

def test_compile_code_double_quotes():
    code = 'print("Hello, World")'
    assert compile_code(docker_client, code) == 'Hello, World'

def test_compile_code_missing_quotes():
    code = 'print("Hello, World)'
    assert compile_code(docker_client, code) != 'Hello, World'

def test_compile_code_multiple_lines():
    code = 'print("Hello, World")\nprint(\'Hello, World\')'
    assert compile_code(docker_client, code) == 'Hello, World\nHello, World'

"""Tests for the grade_submission function"""

def test_grade_submission_no_code():
    assert grade_submission('', '')

def test_grade_submission_matching():
    assert grade_submission('happiness', 'happiness')

def test_grade_submission_not_matching():
    assert not grade_submission('happiness', '')
