from typing import List
from .quiz_model import Quiz, Question, Option

def parse_title(line: str) -> Quiz:
    print(line)
    qtitel = line.removeprefix("# Quiz:").strip()
    print("QTITEL:", qtitel)
    return Quiz(title=qtitel)

def parse_question(line: str, quiz: Quiz) -> Question:
    print(line)
    qtext =  line.split(":", 1)[1].strip()
    question = Question(text=qtext)
    quiz.add_question(question)
    return question

def parse_option(line: str) -> Option:
    print(line)
    correct = line.startswith("- [x]")
    text = line[6:].strip()  # nach "- [x] " oder "- [ ] "
    return Option(text=text, correct=correct)

def parse_quiz(content: str) -> List[Quiz]:
    lines = content.splitlines()
    current_quiz = None
    current_question = None
    result = []

    for line in lines:
        print(line)
        line = line.strip()

        if line.startswith("# Quiz:"):
            current_quiz = parse_title(line)
            result.append(current_quiz)

        elif line.startswith("## Frage"):
            assert current_quiz is not None, \
                f"current_quiz ist None bei dieser Frage: {line}"
            current_question = parse_question(line, current_quiz)

        elif line.startswith("- [x] ") or line.startswith("- [ ] "):
            assert current_question is not None, \
                f"current_question ist None bei dieser Option: {line}"
            current_question.add_option(parse_option(line))

    return result


def print_quiz(quiz: Quiz):
    print("Titel:", quiz.title)
    for i, q in enumerate(quiz.questions, 1):
        print(f"\nFrage {i}: {q.text}")
        for opt in q.options:
            mark = "✅" if opt.correct else "❌"
            print(f"  {mark} {opt.text}")
