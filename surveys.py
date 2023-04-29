from flask import Flask, request, render_template, redirect, flash
from surveys import satisfaction_survey

app = Flask(__name__)

responses = []


@app.route('/')
def survey_home():
    survey_title = "Customer Satisfaction Survey"
    survey_instructions = "Please fill out a survey about your experience with us."
    return render_template('survey_home.html', title=survey_title, instructions=survey_instructions)


if __name__ == '__main__':
    app.run(debug=True)


@app.route('/questions/<int:qid>', methods=['GET', 'POST'])
def show_question(qid):
    """Show the question with the given id."""
    survey = surveys['satisfaction']  # assume satisfaction survey for now

    if qid >= len(survey.questions):
        flash('Invalid question number!')
        return redirect(f'/questions/{len(survey.questions) - 1}')

    question = survey.questions[qid]

    if request.method == 'POST':
        # Append the response to the list of responses
        response = request.form['answer']
        responses.append(response)

        # Check if this is the last question
        if qid == len(survey.questions) - 1:
            return redirect('/thankyou')
        else:
            # Render the next question
            next_qid = qid + 1
            return redirect(f'/questions/{next_qid}')

    # If this is a GET request, render the question template
    return render_template('question.html', question=question, qid=qid)


@app.route('/answer', methods=['POST'])
def handle_answer():
    # Get the answer from the form data
    answer = request.form['answer']

    # Append the answer to the responses list
    responses.append(answer)

    # Get the next question ID
    next_qid = len(responses)

    # If we've answered all questions, redirect to the survey complete page
    if next_qid == len(satisfaction_survey.questions):
        return redirect('/complete')

    # Otherwise, redirect to the next question
    return redirect(f'/questions/{next_qid}')


class Question:
    """Question on a questionnaire."""

    def __init__(self, question, choices=None, allow_text=False):
        """Create question (assume Yes/No for choices."""

        if not choices:
            choices = ["Yes", "No"]

        self.question = question
        self.choices = choices
        self.allow_text = allow_text


class Survey:
    """Questionnaire."""

    def __init__(self, title, instructions, questions):
        """Create questionnaire."""

        self.title = title
        self.instructions = instructions
        self.questions = questions


satisfaction_survey = Survey(
    "Customer Satisfaction Survey",
    "Please fill out a survey about your experience with us.",
    [
        Question("Have you shopped here before?"),
        Question("Did someone else shop with you today?"),
        Question("On average, how much do you spend a month on frisbees?",
                 ["Less than $10,000", "$10,000 or more"]),
        Question("Are you likely to shop here again?"),
    ])

personality_quiz = Survey(
    "Rithm Personality Test",
    "Learn more about yourself with our personality quiz!",
    [
        Question("Do you ever dream about code?"),
        Question("Do you ever have nightmares about code?"),
        Question("Do you prefer porcupines or hedgehogs?",
                 ["Porcupines", "Hedgehogs"]),
        Question("Which is the worst function name, and why?",
                 ["do_stuff()", "run_me()", "wtf()"],
                 allow_text=True),
    ]
)

surveys = {
    "satisfaction": satisfaction_survey,
    "personality": personality_quiz,
}
