from flask import Flask, render_template, request, redirect, url_for
import data_manager, util

app = Flask(__name__)


@app.route('/list')
def all_questions(limit=None):
    questions = data_manager.get_all_questions(limit)
    return render_template('index.html', questions=questions)

@app.route('/')
def latest_questions(limit=5):
    questions = data_manager.get_all_questions(limit)
    return render_template('index.html', questions=questions)

@app.route('/add-question', methods=['GET', 'POST'])
def save_new_question():
    if request.method == 'POST':
        new_question_data = {
            "submission_time": util.create_timestamp(),
            "view_number": "0",
            "vote_number": "0",
            "title": request.form.get('title'),
            "message": request.form.get('message'),
        }
        data_manager.save_new_question(new_question_data)
        return redirect(url_for('question_details',question_id=data_manager.get_max_id()),question_headers=data_manager.QUESTION_HEADER)
    return render_template('add_question.html')


@app.route('/question/<question_id>')
def question_details(question_id):
    questions = data_manager.get_all_questions()
    for question in questions:
        if int(question_id) == question.get('id'):
            question_details = question.values()
    return render_template(
        'question-details.html', question=question_details,
        question_id=question_id,
        answers=data_manager.get_all_answers()
    )


@app.route('/question/<question_id>/new-answer', methods=['GET', 'POST'])
def add_answer(question_id):
    if request.method == 'POST':
        new_answer_data = {
            "submission_time": util.create_timestamp(),
            "vote_number": "0",
            "question_id":question_id,
            "message": request.form.get('message'),
            "image": "n/a"
        }
        data_manager.save_new_answer(new_answer_data)
        route = f"/question/{str(question_id)}"
        return redirect(route)
    elif request.method == 'GET':
        return render_template('add_answer.html',question_id=question_id)


if __name__ == '__main__':
    app.run(debug=True,port=8000)
