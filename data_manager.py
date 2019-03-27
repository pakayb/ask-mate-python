import connection
import database_common

ANSWER_FILE_PATH = 'answer.csv'
QUESTION_FILE_PATH = 'question.csv'
ANSWER_HEADER = ['id', 'submission_time', 'vote_number', 'question_id', 'message', 'image']
QUESTION_HEADER = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']


@database_common.connection_handler
def get_all_questions(cursor,limit=None):
    cursor.execute("""
                    SELECT * FROM question
                    ORDER BY submission_time DESC
                    LIMIT %(limit)s
                    """,{'limit':limit})
    questions = cursor.fetchall()
    return questions


@database_common.connection_handler
def save_new_question(cursor,data):
    cursor.execute("""
                    INSERT INTO question (submission_time, view_number, vote_number, title, message)  
                    VALUES (%s, %s, %s, %s, %s)
    """, (data.get('submission_time'), data.get('view_number'), data.get('vote_number'), data.get('title'), data.get('message')))


@database_common.connection_handler
def get_max_id(cursor):
    cursor.execute("""
                    SELECT id FROM question
                    ORDER BY id DESC 
                    LIMIT 1
    """)
    max_id = cursor.fetchone()
    return max_id.get('id')


@database_common.connection_handler
def save_new_answer(cursor, data):
    # connection.append_item_to_csv(ANSWER_FILE_PATH, ANSWER_HEADER, value)
    cursor.execute("""
                    INSERT INTO answer (submission_time, vote_number, question_id, message)  
                    VALUES (%s, %s, %s, %s)
    """, (data.get('submission_time'), data.get('vote_number'), data.get('question_id'), data.get('message')))


@database_common.connection_handler
def update_view_number(cursor,number):
    cursor.execute("""
                    UPDATE question SET view_number = %(views)s
    """,{'views':number})


@database_common.connection_handler
def get_all_answers(cursor):
    # return connection.read_csv(ANSWER_FILE_PATH, ANSWER_HEADER)
    cursor.execute("""
                        SELECT * FROM answer
                        ORDER BY submission_time DESC
                        """)
    return cursor.fetchall()


@database_common.connection_handler
def get_searched_questions(cursor, keyword):
    cursor.execute("""
                        SELECT DISTINCT question.* FROM answer
                        JOIN question ON answer.question_id = question.id
                        WHERE answer.message ILIKE %(keyword)s OR question.title ILIKE %(keyword)s OR question.message ILIKE %(keyword)s
                """,
                   {'keyword':keyword})
    return cursor.fetchall()


@database_common.connection_handler
def update_answer(cursor,answer):
    cursor.execute("""
                    UPDATE question SET message = %(answer)s 
    """,
                   {'answer':answer})

# @database_common.connection_handler
# def get_question_headers(cursor):
#     cursor.execute("""
#                     SELECT * FROM information_schema.columns
#                     WHERE TABLE_NAME =N'question'
#     """)
#     question_header = cursor.fetchall()
#     return question_header
#
#
# def get_answer_headers():
#     answer_header = [header.title().replace("_", " ") for header in ANSWER_HEADER]
#     return answer_header
