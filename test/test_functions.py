"""Unit tests for the parser module"""

from duel.functions import compile_code, grade_submission

import docker

docker_client = docker.Client(base_url='tcp://alphadev:2375')

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

def test_grade_submission_no_code():
    assert grade_submission('', '')

def test_grade_submission_matching():
    assert grade_submission('happiness', 'happiness')

def test_grade_submission_not_matching():
    assert not grade_submission('happiness', '')
