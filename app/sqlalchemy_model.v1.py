from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Quiz(Base):
    __tablename__ = "quiz"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)

    questions = relationship("Question", back_populates="quiz", cascade="all, delete-orphan")

    def add_question(self, q: "Question"):
        self.questions.append(q)

class Question(Base):
    __tablename__ = "question"

    id = Column(Integer, primary_key=True)
    text = Column(String, nullable=False)
    quiz_id = Column(Integer, ForeignKey("quiz.id"))

    quiz = relationship("Quiz", back_populates="questions")
    options = relationship("Option", back_populates="question", cascade="all, delete-orphan")

    def add_option(self, opt: "Option"):
        self.options.append(opt)

class Option(Base):
    __tablename__ = "option"

    id = Column(Integer, primary_key=True)
    text = Column(String, nullable=False)
    correct = Column(Boolean, default=False)
    question_id = Column(Integer, ForeignKey("question.id"))

    question = relationship("Question", back_populates="options")
