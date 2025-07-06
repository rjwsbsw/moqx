from fastapi import FastAPI, Request, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from quiz_schema import QuizOut
from quiz_parser_md import parse_quiz
import sqlalchemy_process as db


app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    quizzes = db.load_all_quizzes()
    return templates.TemplateResponse("index.html", {
        "request": request,
        "quizzes": quizzes
    })


@app.get("/quiz/{quiz_id}", response_class=HTMLResponse)
def show_quiz(request: Request, quiz_id: int):
    quiz = db.load_quiz_by_id(quiz_id)
    schema = QuizOut.from_orm(quiz)
    return templates.TemplateResponse("quiz.html", {
        "request": request,
        "quiz": schema
    })

@app.post("/submit", response_class=HTMLResponse)
async def submit(request: Request):
    form = await request.form()
    selected_ids = [int(value) for _,value in form.multi_items()] # alle ausgewählten Option-IDs
    options = db.load_options_by_ids(selected_ids)
    print(options)

    # Optionen nach Frage gruppieren
    result_by_question = {}
    for opt in options:
        if opt.question_id not in result_by_question:
            result_by_question[opt.question_id] = []
        result_by_question[opt.question_id].append(opt)
    print(result_by_question)

    score = 0
    results = []
    questions = db.load_questions_by_ids(list(result_by_question.keys()))

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

@app.get("/upload", response_class=HTMLResponse)
def upload_form(request: Request):
    return templates.TemplateResponse("upload.html", {"request": request})

@app.post("/upload", response_class=HTMLResponse)
async def upload_file(request: Request, file: UploadFile = File(...)):
    content = await file.read()
    text = content.decode("utf-8")
    
    try:
        parsed_quizzes = parse_quiz(text)
        count = db.upload_parsed_quizzes(parsed_quizzes)
    except Exception as e:
        return templates.TemplateResponse("upload_reply.html", {
            "request": request,
            "answer": "error",
            "error": str(e)
        })

    return templates.TemplateResponse("upload_reply.html", {
        "request": request,
        "answer": "success",
        "filename": file.filename,
        "imported": count,
    })