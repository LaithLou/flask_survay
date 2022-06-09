from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)


@app.get("/")
def show_survey():
    """Homepage is rendered with with start information about survey and start button,
    initiates session"""
    session["responses"] = []
    return render_template("survey_start.html", survey=survey)


@app.post('/begin')
def start_survey():
    """takes in a post request to clear responses global variable
    and redircts to questions page"""

    q_id = 0
    return redirect(f"/questions/{q_id}")


@app.get("/questions/<int:q_id>")
def ask_question(q_id):
    """takes in an ID and updates question route to reflect corresponding question
    and returns that page, checks if user is trying to access wrong question route and
    redircts them if they are with a flash message"""

    responses = session['responses']
    if len(responses) == len(survey.questions):
        flash("you've already answered all the question")
        return redirect('/complete')
    elif not q_id == len(responses):
        q_id = len(responses)
        flash("please answer the questions in order")
        return redirect(f"/questions/{q_id}")

    return render_template("question.html", question=survey.questions[q_id])


@app.post('/answer')
def get_answer():
    """stores submited answer in a session and updates question route and
    redircts to question request or redirects to completion page
    when all questions are answered"""

    responses = session['responses']
    responses.append(request.form['answer'])
    session['responses'] = responses
    q_id = len(responses)
    if q_id < len(survey.questions):
        return redirect(f"/questions/{q_id}")
    else:
        return redirect('/complete')

@app.get('/complete')
def get_complete_stage():
    """display completion page"""
    print(session['responses'])
    return render_template('completion.html')
