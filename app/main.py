import sys
from pathlib import Path
from quiz_parser_md import parse_quiz, print_quiz
from sqlalchemy_model import Quiz, Question, Option
from db_utils import get_engine, create_db, get_session

def lese_quiz() -> str:
    if len(sys.argv) < 2:
        print("❌ Fehler: Bitte gib den Pfad zur Markdown-Datei an.")
        print("👉 Beispiel: python main.py quiz.md")
        sys.exit(1)

    filepath = Path(sys.argv[1])
    if not filepath.exists():
        print(f"❌ Datei nicht gefunden: {filepath}")
        sys.exit(1)

    return filepath.read_text(encoding="utf-8")

def main():
    content = lese_quiz()
    parsed_quizzes = parse_quiz(content)

    engine = get_engine()
    create_db(engine)
    session = get_session(engine)

    for quiz in parsed_quizzes:
        db_quiz = Quiz(title=quiz.title)
        for q in quiz.questions:
            db_q = Question(text=q.text)
            for opt in q.options:
                db_q.options.append(Option(text=opt.text, correct=opt.correct))
            db_quiz.questions.append(db_q)
        session.add(db_quiz)

    session.commit()
    print("✅ Quiz wurde erfolgreich gespeichert.")

    # 🔍 Jetzt: Daten direkt aus der DB lesen und anzeigen
    print("\n📤 Gespeicherte Inhalte aus der Datenbank:")
    for quiz in session.query(Quiz).all():
        print_quiz(quiz)

if __name__ == "__main__":
    main()
