from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)
responses = []


@app.get("/")
def show_survey():
    """Homepage is rendered with with start information about survey and start button"""

    return render_template("survey_start.html", survey=survey)


@app.post('/begin')
def start_survay():
    """takes in a post request to clear responses global variable
    and redircts to questions page"""

    responses.clear()
    id = len(responses)
    return redirect(f"/questions/{id}")


@app.get("/questions/<int:id>")
def ask_question(id):
    """takes in an ID and updates question route to reflect corresponding question
    and returns that page"""

    return render_template("question.html", question=survey.questions[id])


@app.post('/answer')
def get_answer():
    """stores submited answer and updates question route and redircts to question request
    or shows completion page when all questions are answered"""

    responses.append(request.form['answer'])
    id = len(responses)
    if id < len(survey.questions):
        return redirect(f"/questions/{id}")
    else:
        return render_template('completion.html')
