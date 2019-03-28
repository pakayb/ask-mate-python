from flask import Flask, render_template, request, redirect, url_for
import data_manager, util

app = Flask(__name__)


@app.route('/list')
def all_questions(limit=None):
    questions = data_manager.get_all_questions(limit)
    return render_template('index.html', questions=questions, header='List of all questions')


@app.route('/')
def latest_questions(limit=5):
    questions = data_manager.get_all_questions(limit)
    return render_template('index.html', questions=questions, header='Latest questions')


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
        return redirect(url_for('question_details',question_id=data_manager.get_max_id()))
    return render_template('add_question.html')


@app.route('/question/<question_id>')
def question_details(question_id):
    questions = data_manager.get_all_questions()
    for question in questions:
        if int(question_id) == question.get('id'):
            question_details = question.values()
            view_number = question.get('view_number') + 1
    data_manager.update_view_number(view_number)
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


@app.route('/answer/<answer_id>/edit', methods=['GET', 'POST'])
def update_answer(answer_id):
    answers = data_manager.get_all_answers()
    for answer in answers:
        if int(answer_id) == answer.get('id'):
            answer_message = answer.get('message')
            question_id = answer.get('question_id')
    if request.method == 'GET':
        return render_template('add_answer.html', answer=answer_message, answer_id=answer_id)
    elif request.method == 'POST':
        data_manager.update_answer(request.form.get('message'), answer_id)
        return redirect(url_for('question_details', question_id=question_id))


@app.route('/search')
def searching():
    search_key = '%'+request.args.get('search_key')+'%'
    questions = data_manager.get_searched_questions(search_key)
    return render_template('index.html', questions=questions, header='Search result')


@app.route('/question/<answer_id>/new-comment', methods=['GET', 'POST'])
@app.route('/question/<question_id>/new-comment', methods=['GET', 'POST'])
def add_comment(answer_id=None, question_id=None):
    if request.method == 'POST':
        new_comment_data = {
            "question_id": question_id,
            "answer_id": answer_id,
            "message": request.form.get('message'),
            "submission_time": util.create_timestamp(),
            "edited_count": 0
        }
        data_manager.add_comment(new_comment_data)
        return render_template('kacsa.html', comments=data_manager.get_all_comments())
    elif request.method == 'GET':
        return render_template('add_comment.html', question_id=question_id, header='ASD')


if __name__ == '__main__':
    app.run(debug=True, port=8000)
