from flask import Flask, render_template, request, redirect, url_for, session, escape
import data_manager, util
import bcrypt

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


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
        return redirect(url_for('question_details', question_id=data_manager.get_max_id()))
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
        answers=data_manager.get_all_answers(),
        comments=data_manager.get_all_comments()
    )


@app.route('/question/<question_id>/new-answer', methods=['GET', 'POST'])
def add_answer(question_id):
    if request.method == 'POST':
        new_answer_data = {
            "submission_time": util.create_timestamp(),
            "vote_number": "0",
            "question_id": question_id,
            "message": request.form.get('message'),
            "image": "n/a"
        }
        data_manager.save_new_answer(new_answer_data)
        route = f"/question/{str(question_id)}"
        return redirect(route)
    elif request.method == 'GET':
        return render_template('add_answer.html', question_id=question_id)


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
    search_key = '%' + request.args.get('search_key') + '%'
    questions = data_manager.get_searched_questions(search_key)
    return render_template('index.html', questions=questions, header='Search result')


@app.route('/answer/<answer_id>/new-comment', methods=['GET', 'POST'])
def add_comment_to_answer(answer_id=None, question_id=None):
    if request.method == 'POST':
        new_comment_data = {
            "question_id": question_id,
            "answer_id": answer_id,
            "message": request.form.get('message'),
            "submission_time": util.create_timestamp(),
            "edited_count": 0
        }
        data_manager.add_comment(new_comment_data)
        redirect_id = request.form.get('redirect_id')
        return redirect(url_for('question_details', question_id=redirect_id))
    elif request.method == 'GET':
        answers = data_manager.get_all_answers()
        for answer in answers:
            if int(answer_id) == answer.get('id'):
                redirect_id = answer.get('question_id')
        return render_template('add_answer_comment.html', answer_id=answer_id, redirect_id=redirect_id)


@app.route('/question/<question_id>/new-comment', methods=['GET', 'POST'])
def add_comment_to_question(answer_id=None, question_id=None):
    if request.method == 'POST':
        new_comment_data = {
            "question_id": question_id,
            "answer_id": answer_id,
            "message": request.form.get('message'),
            "submission_time": util.create_timestamp(),
            "edited_count": 0
        }
        data_manager.add_comment(new_comment_data)
        return redirect(url_for('question_details', question_id=question_id))
    elif request.method == 'GET':
        return render_template('add_comment.html', question_id=question_id)


@app.route('/login/user')
def index():
    if 'username' in session:
        return 'Logged in as %s' % escape(session['username'])
    return 'You are not logged in'


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        plain_text_password = request.form['password']
        passwd = data_manager.get_password_by_username(session['username']).get('password')
        print(verify_password(plain_text_password,passwd))
        if verify_password(plain_text_password,passwd ):
            return redirect('/login/user')
        else:
            return redirect(url_for('login'))
    return render_template('registration.html')


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))


def verify_password(plain_text_password, hashed_password):
    hashed_bytes_password = hashed_password.encode('utf-8')
    return bcrypt.checkpw(plain_text_password.encode('utf-8'), hashed_bytes_password)

 
def create_user_data():
    passwd = hash_password(request.form.get('password'))
    user_data = {
        'user_name': request.form.get('username'),
        'password': passwd,
        'registration_time': util.create_timestamp()
    }
    return user_data


@app.route('/registration', methods=['GET', 'POST'])
def save_new_user():
    if request.method == 'POST':
        data_manager.add_new_user(create_user_data())
        return redirect('/')
    return render_template('registration.html')


def hash_password(plain_text_password):
    hashed_bytes = bcrypt.hashpw(plain_text_password.encode('utf-8'), bcrypt.gensalt())
    return hashed_bytes.decode('utf-8')


if __name__ == '__main__':
    app.run(debug=True, port=8000)

