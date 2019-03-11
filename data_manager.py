import connection

ANSWER_FILE_PATH = 'answer.csv'
QUESTION_FILE_PATH = 'question.csv'
ANSWER_HEADER = ['id', 'submission_time', 'vote_number', 'question_id', 'message', 'image']
QUESTION_HEADER = ['id', 'submision_time', 'view_number', 'vote_number', 'title', 'message', 'image']

def save_new_question(value):
    connection.append_item_to_csv(QUESTION_FILE_PATH, QUESTION_HEADER, value)