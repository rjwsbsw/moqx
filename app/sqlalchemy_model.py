from typing import List
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass

class Quiz(Base):
    __tablename__ = "quiz"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String, nullable=False)

    questions: Mapped[List["Question"]] = relationship(
        back_populates="quiz",
        cascade="all, delete-orphan"
    )

    def add_question(self, q: "Question"):
        self.questions.append(q)

class Question(Base):
    __tablename__ = "question"

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(String, nullable=False)
    quiz_id: Mapped[int] = mapped_column(ForeignKey("quiz.id"))

    quiz: Mapped["Quiz"] = relationship(back_populates="questions")
    options: Mapped[List["Option"]] = relationship(
        back_populates="question",
        cascade="all, delete-orphan"
    )

    def add_option(self, opt: "Option"):
        self.options.append(opt)

class Option(Base):
    __tablename__ = "option"

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(String, nullable=False)
    correct: Mapped[bool] = mapped_column(default=False)
    question_id: Mapped[int] = mapped_column(ForeignKey("question.id"))

    question: Mapped["Question"] = relationship(back_populates="options")

