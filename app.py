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
    return render_template("survey_start.html", survey=survey)


@app.post('/begin')
def start_survay():

    return redirect('/questions/0')


@app.get("/questions/<int:id>")
def ask_question(id):

    return render_template("question.html", question=survey.questions[id])


@app.post('/answer')
def get_answer():

    responses.append(request.form['answer'])
    id = len(responses)
    if id < len(survey.questions):
        return redirect(f"/questions/{id}")
    else:
        return render_template('completion.html')
