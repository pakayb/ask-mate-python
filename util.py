import time,datetime,data_manager
from operator import itemgetter


def create_timestamp():
    return datetime.datetime.now()


def convert_timestamp(timestamp):
    return datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')


def question_next_id():
    questions = data_manager.get_all_questions()
    try:
        next_id = max(int(id) for id in questions.keys())
        return next_id+1
    except ValueError:
        return 1


# def sorting_by_time():
#     questions = data_manager.get_all_questions()
#     questions = [question for question in questions.values()]
#     questions = sorted(questions,key=itemgetter(1), reverse=True)
#     sorted_questions = {questions[i][0]: line for i, line in enumerate(questions)}
#     return sorted_questions


# def sorting_answers_by_time():
#     answers = data_manager.get_all_answers()
#     answers = [answer for answer in answers]
#     answers = sorted(answers,key=itemgetter(1), reverse=True)
#     sorted_answers = {answers[i][0]: line for i, line in enumerate(answers)}
#     return sorted_answers


def answer_next_id():
    answers = data_manager.get_all_answers()
    try:
        next_id = max(int(id) for id in answers.keys())
        return next_id+1
    except ValueError:
        return 1
