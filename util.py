import time,datetime


def create_timestamp():
    return int(time.time())


def convert_timestamp(timestamp):
    return datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')


def question_maximum_id():
    questions = data.manager.get_all_question()
    try:
        maximum_id = max(int(questions.keys()))
        return maximum_id
    except ValueError:
        return 0
