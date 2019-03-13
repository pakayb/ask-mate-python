from flask import Flask, render_template, request, redirect, url_for
import data_manager, util

app = Flask(__name__)


@app.route('/')
@app.route('/list')
def all_questions():
    questions = util.sorting_by_time()

    return render_template('index.html', questions=questions)


@app.route('/add-question', methods=['GET', 'POST'])
def save_new_question():
    if request.method == 'POST':
        new_question_data = {
            "id": util.question_next_id(),
            "submission_time": util.create_timestamp(),
            "view_number": "0",
            "vote_number": "0",
            "title": request.form.get('title'),
            "message": request.form.get('message'),
            "image": "n/a"
        }
        data_manager.save_new_question(new_question_data)
        return redirect("/list")
    return render_template('add_question.html')


@app.route('/question/<question_id>')
def question_details(question_id):
    questions = data_manager.get_all_questions()
    question = questions[question_id]
    return render_template('question-details.html', question=question, headers=data_manager.get_question_headers())


@app.route('/question/<question_id>/new-answer')
def add_answer(question_id):
    render_template('add_answer.html', answer_id=question_id)


if __name__ == '__main__':
    app.run(debug=True)
