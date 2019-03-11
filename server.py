from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


@app.route('/')
def all_questions():
    questions = data_manager.get_all_questions()

    return render_template('index.html', questions=questions)


@app.route('/save-new-question', methods=['POST'])
def save_new_question():
    new_question_data = {
        "title": request.form.get('title', 'n/a')
    }

    # ugly: new_question_data = request.form.to_dict()

    data_manager.save_new_question(new_question_data)

    return redirect(url_for('all_questions'))
