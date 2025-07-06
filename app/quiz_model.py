# file: quiz_model.py

from typing import List

class Option:
    def __init__(self, text: str, correct: bool):
        self.text = text
        self.correct = correct

class Question:
    def __init__(self, text: str):
        self.text = text
        self.options: List[Option] = []

    def add_option(self, option: Option):
        self.options.append(option)

class Quiz:
    def __init__(self, title: str):
        self.title = title
        self.questions: List[Question] = []

    def add_question(self, question: Question):
        self.questions.append(question)
