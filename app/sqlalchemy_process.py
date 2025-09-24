import time
import logging

from .sqlalchemy_model import Quiz, Question, Option
from .db_utils import get_engine, get_session, create_db, OperationalError


# DB initialisieren
def _init_db_():
    engine = get_engine()
    create_db(engine)
    return get_session(engine)

# neue init_db mit Retry und Logging
def init_db(retries=5, delay=3):
    last_exception = None
    for attempt in range(1, retries + 1):
        try:
            return _init_db_()
        except OperationalError as e:
            logging.error(f"🔁 DB-Verbindung fehlgeschlagen (Versuch {attempt}/{retries}): {e}")
            last_exception = e
            time.sleep(delay)
    logging.error("❌ Alle Verbindungsversuche fehlgeschlagen.")
    raise last_exception

# 📥 importiere geparste Quizzes in die DB
def upload_parsed_quizzes(parsed_quizzes):
    session = init_db()

    for quiz in parsed_quizzes:
        db_quiz = Quiz(title=quiz.title)
        for q in quiz.questions:
            db_q = Question(text=q.text)
            for opt in q.options:
                db_q.add_option(Option(text=opt.text, correct=opt.correct))
            db_q.text = q.text
            db_quiz.add_question(db_q)
        session.add(db_quiz)

    session.commit()
    return len(parsed_quizzes)

# 📋 lade alle Quizzes für die Startseite
def load_all_quizzes():
    session = init_db()
    return session.query(Quiz).all()

# 🔍 lade ein Quiz per ID für Anzeige/Auswertung
def load_quiz_by_id(quiz_id: int):
    session = init_db()
    return session.query(Quiz).get(quiz_id)

# 📊 lade ausgewählte Optionen für Auswertung
def load_options_by_ids(option_ids: list[int]):
    session = init_db()
    return session.query(Option).filter(Option.id.in_(option_ids)).all()

# 🔁 lade Fragen für Auswertung
def load_questions_by_ids(question_ids: list[int]):
    session = init_db()
    return session.query(Question).filter(Question.id.in_(question_ids)).all()

def delete_quizzes_by_ids(quiz_ids: list[int]):
    session = init_db()
    for qid in quiz_ids:
        quiz = session.get(Quiz, qid)
        if quiz:
            session.delete(quiz)
    session.commit()
