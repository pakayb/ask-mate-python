import connection

ANSWER_FILE_PATH = 'answer.csv'
QUESTION_FILE_PATH = 'question.csv'
ANSWER_HEADER = ['id', 'submission_time', 'vote_number', 'question_id', 'message', 'image']
QUESTION_HEADER = ['id', 'submision_time', 'view_number', 'vote_number', 'title', 'message', 'image']

def save_new_question(value):
    connection.append_item_to_csv(QUESTION_FILE_PATH, QUESTION_HEADER, value)

def save_new_answer(value):
    connection.append_item_to_csv(ANSWER_FILE_PATH, ANSWER_HEADER, value)

def get_all_questions():
    return connection.read_csv(QUESTION_FILE_PATH, QUESTION_HEADER)

def get_all_answers():
    return connection.read_csv(ANSWER_FILE_PATH, ANSWER_HEADER)