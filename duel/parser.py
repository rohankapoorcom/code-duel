"""
Contains the QuestionParser class which loads in all of the Project Euler data
"""

from duel import db
from duel.models import Source, Question

import linecache

class QuestionParser:
    """Parses all the Project Euler data"""

    def __init__(self, question_file, answer_file):
        """Initializes a new Project Euler Parser"""
        self._question_file = question_file
        self._answer_file = answer_file

    def parse(self, total_questions):
        """Parses the specified number of questions from a Project Euler dataset"""
        source = Source('Project Euler')
        db.session.add(source)
        for i in range(total_questions):
            problem_lines = [line for line in self.parse_question(i)]
            answer = self.parse_answer(i).decode('utf-8')
            question = Question('\n'.join(problem_lines[3:]).decode('utf-8'), answer, source)
            db.session.add(question)

        db.session.commit()

    def parse_question(self, question_number):
        """Parses the specified question number"""
        with open(self._question_file) as file:
            problemText = False
            lastLine = ''

            for line in file:
                if line.strip() == 'Problem {}'.format(question_number + 1):
                    problemText = True

                if problemText:
                    if line == lastLine == '\n':
                        break
                    else:
                        yield line[:-1]
                        lastLine = line

    def parse_answer(self, question_number):
        """Parses the specific answer"""
        try:
            return linecache.getline(self._answer_file, question_number + 1).split('. ')[1].strip()
        except Exception, e:
            raise
