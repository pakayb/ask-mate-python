import connection

ANSWER_FILE_PATH = 'answer.csv'
QUESTION_FILE_PATH = 'question.csv'
ANSWER_HEADER = ['id', 'submission_time', 'vote_number', 'question_id', 'message', 'image']
QUESTION_HEADER = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']


def save_new_question(value):
    connection.append_item_to_csv(QUESTION_FILE_PATH, QUESTION_HEADER, value)


def save_new_answer(value):
    connection.append_item_to_csv(ANSWER_FILE_PATH, ANSWER_HEADER, value)


def get_all_questions():
    return connection.read_csv(QUESTION_FILE_PATH, QUESTION_HEADER)


def get_all_answers():
    return connection.read_csv(ANSWER_FILE_PATH, ANSWER_HEADER)


def get_question_headers():
    question_header = [header.title().replace("_", " ") for header in QUESTION_HEADER]
    return question_header


def get_answer_headers():
    answer_header = [header.title().replace("_", " ") for header in ANSWER_HEADER]
    return answer_header
