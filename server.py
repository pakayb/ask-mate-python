from flask import Flask, render_template, request, redirect, url_for, session, escape
import data_manager, util
import bcrypt

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


@app.route('/list')
def all_questions(limit=None):
    questions = data_manager.get_all_questions(limit)
    return render_template('index.html', questions=questions, header='List of all questions', login=get_user_id())


@app.route('/')
def latest_questions(limit=5):
    questions = data_manager.get_all_questions(limit)
    return render_template('index.html', questions=questions, header='Latest questions', login=get_user_id())


@app.route('/add-question', methods=['GET', 'POST'])
def save_new_question():
    if request.method == 'POST':
        data_manager.save_new_question(stion_data())
        return redirect(url_for('question_details', question_id=data_manager.get_max_id()))
    return render_template('add_question.html')


def create_new_question_data():
    new_question_data = {
        "submission_time": util.create_timestamp(),
        "view_number": "0",
        "vote_number": "0",
        "title": request.form.get('title'),
        "message": request.form.get('message'),
        "user_id": get_user_id()
    }
    return new_question_data


@app.route('/question/<question_id>')
def question_details(question_id):
    question = data_manager.get_question_by_id(question_id)
    data_manager.update_view_number(question.get('view_number'),question_id)
    return render_template(
        'question-details.html', question=question,
        question_id=question_id,
        answers=data_manager.get_all_answers(),
        comments=data_manager.get_all_comments(),
        login=get_user_id()
    )


@app.route('/question/<question_id>/new-answer', methods=['GET', 'POST'])
def add_answer(question_id):
    if request.method == 'POST':
        data_manager.save_new_answer(create_new_answer_data(question_id))
        return redirect(url_for('question_details',question_id=question_id))
    elif request.method == 'GET':
        return render_template('add_answer.html', question_id=question_id)


def create_new_answer_data(question_id):
    new_answer_data = {
        "submission_time": util.create_timestamp(),
        "vote_number": "0",
        "question_id": question_id,
        "message": request.form.get('message'),
        "image": "n/a",
        "user_id": get_user_id()
    }
    return new_answer_data


@app.route('/answer/<answer_id>/edit', methods=['GET', 'POST'])
def update_answer(answer_id):
    answer = data_manager.get_answer_by_id(answer_id)
    if request.method == 'GET':
        return render_template('add_answer.html', answer=answer.get('message'), answer_id=answer.get('id'))
    elif request.method == 'POST':
        data_manager.update_answer(request.form.get('message'), answer_id)
        return redirect(url_for('question_details', question_id=answer.get('question_id')))


@app.route('/search')
def searching():
    search_key = '%' + request.args.get('search_key') + '%'
    questions = data_manager.get_searched_questions(search_key)
    return render_template('index.html', questions=questions, header='Search result')


@app.route('/answer/<answer_id>/new-comment', methods=['GET', 'POST'])
def add_comment_to_answer(answer_id=None, question_id=None):
    if request.method == 'POST':
        data_manager.add_comment(create_new_comment_data(answer_id, question_id))
        return redirect(url_for('question_details', question_id=request.form.get('redirect_id')))
    elif request.method == 'GET':
        answer = data_manager.get_answer_by_id(answer_id)
        return render_template('add_answer_comment.html', answer_id=answer_id, redirect_id=answer.get('question_id'))


def create_new_comment_data(answer_id, question_id):
    new_comment_data = {
        "question_id": question_id,
        "answer_id": answer_id,
        "message": request.form.get('message'),
        "submission_time": util.create_timestamp(),
        "edited_count": 0,
        "user_id": get_user_id()
    }
    return new_comment_data


@app.route('/question/<question_id>/new-comment', methods=['GET', 'POST'])
def add_comment_to_question(answer_id=None, question_id=None):
    if request.method == 'POST':
        data_manager.add_comment(create_new_comment_data(answer_id,question_id))
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
            try:
                passwd = data_manager.get_password_by_username(session['username']).get('password')
            except AttributeError:
                return render_template('registration.html', alert=True)
            if verify_password(plain_text_password, passwd):
                return redirect(request.form['referrer'])
            return render_template('registration.html', alert=True)
    nexturl = request.referrer
    return render_template('registration.html', nexturl=nexturl)


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('latest_questions'))


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


@app.route('/list_users')
def list_all_users():
    users = data_manager.list_all_user()
    return render_template('all_users.html', users=users)


def get_user_id():
    try:
        user = data_manager.get_id_by_user_name(session['username'])
        return user['id']
    except KeyError:
        return None


if __name__ == '__main__':
    app.run(debug=True, port=8000)

