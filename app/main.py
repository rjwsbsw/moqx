from pathlib import Path

from fastapi import FastAPI, Request, UploadFile, File
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from .db_utils import OperationalError
from .quiz_schema import QuizOut
from .quiz_parser_md import parse_quiz
from .sqlalchemy_process import load_all_quizzes, upload_parsed_quizzes, delete_quizzes_by_ids
from .sqlalchemy_process import load_questions_by_ids, load_quiz_by_id, load_options_by_ids

api = FastAPI()
BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=BASE_DIR / "templates")

@api.get("/", response_class=HTMLResponse)
def index(request: Request):
    """
    Show all available quizzes.

    Returns a HTML page with a list of links to available quizzes.
    """
    error_msg = ""
    try:
        quizzes = load_all_quizzes()
    except OperationalError as e:
        error_msg = str(e)
        quizzes = []
    return templates.TemplateResponse("index.html", {
        "request": request,
        "errorMsg": error_msg,
        "quizzes": quizzes
    })


@api.get("/quiz/{quiz_id}", response_class=HTMLResponse)
def show_quiz(request: Request, quiz_id: int):
    quiz = load_quiz_by_id(quiz_id)
    schema = QuizOut.model_validate(quiz)
    return templates.TemplateResponse("quiz.html", {
        "request": request,
        "quiz": schema
    })

@api.post("/submit", response_class=HTMLResponse)
async def submit(request: Request):
    form = await request.form()
    selected_ids = [int(value) for _,value in form.multi_items()] # alle ausgewählten Option-IDs
    options = load_options_by_ids(selected_ids)
    # print("DEBUG Option: %s" % (options,))
    # for opt in options:
    #     print("DEBUG Option:", opt.id, opt.text, opt.correct, opt.question_id)


    # Optionen nach Frage gruppieren
    result_by_question = {}
    for opt in options:
        if opt.question_id not in result_by_question:
            result_by_question[opt.question_id] = []
        result_by_question[opt.question_id].append(opt)
    print(result_by_question)

    score = 0
    results = []
    questions = load_questions_by_ids(list(result_by_question.keys()))

    for q in questions:
        selected_os = result_by_question.get(q.id, [])
        correct_os = [o for o in q.options if o.correct]
        is_correct = set(o.id for o in selected_os) == set(o.id for o in correct_os)

        results.append({
            "question": q.text,
            "selected": selected_os,
            "correct": correct_os,
            "is_correct": is_correct
        })

        if is_correct:
            score += 1

    return templates.TemplateResponse("result.html", {
        "request": request,
        "score": score,
        "max_score": len(questions),
        "results": results
    })

@api.get("/upload", response_class=HTMLResponse)
def upload_form(request: Request):
    return templates.TemplateResponse("upload.html", {"request": request})

@api.post("/upload", response_class=HTMLResponse)
async def upload_file(request: Request, file: UploadFile = File(...)):
    content = await file.read()
    text = content.decode("utf-8")
    error_msg, count = "", 0
    
    try:
        #print("Parsing: %s" % text)
        parsed_quizzes = parse_quiz(text)
        print("Parsed Quizzes: %s", parsed_quizzes)
    except Exception as e:
        error_msg =f"""
            Unerwarteter Fehler beim Parsen:\n
            Error: {str(e)}"""
    if not error_msg:
        try:
            count = upload_parsed_quizzes(parsed_quizzes)
        except Exception as e:
            error_msg =f"""
                Unerwarteter Fehler beim Speichern:\n
                Error: {str(e)}"""

    return templates.TemplateResponse("upload_reply.html", {
        "request": request,
        "answer": "success" if error_msg == "" else "error",
        "filename": file.filename,
        "imported": count,
        "error": error_msg,
        "errorMsg": error_msg
    })


@api.get("/delete")
def show_delete_page(request: Request):
    quizzes = load_all_quizzes()
    return templates.TemplateResponse("delete_quizzes.html", {
        "request": request,
        "quizzes": quizzes
    })

@api.post("/delete")
async def delete_selected_quizzes(request: Request):
    form = await request.form()
    ids = [int(value) for key, value in form.multi_items() if key == "quiz_id"]
    delete_quizzes_by_ids(ids)
    return RedirectResponse(url="/", status_code=303)
