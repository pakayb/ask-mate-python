import database_common


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
                    INSERT INTO question (submission_time, view_number, vote_number, title, message, user_id)  
                    VALUES (%s, %s, %s, %s, %s, %s)
    """, (data.get('submission_time'), data.get('view_number'), data.get('vote_number'), data.get('title'), data.get('message'), data.get('user_id')))


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
    cursor.execute("""
                    INSERT INTO answer (submission_time, vote_number, question_id, message, user_id)  
                    VALUES (%s, %s, %s, %s, %s)
    """, (data.get('submission_time'), data.get('vote_number'), data.get('question_id'), data.get('message'), data.get('user_id')))


@database_common.connection_handler
def update_view_number(cursor,number,question_id):
    cursor.execute("""
                    UPDATE question SET view_number = %(number)s
                    WHERE id = %(question_id)s
    """,{'number':number + 1,'question_id':question_id})


@database_common.connection_handler
def get_all_answers(cursor):
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
def update_answer(cursor, answer, answer_id):
    cursor.execute("""
                    UPDATE answer SET message = %(answer)s
                    WHERE id = %(answer_id)s
    """,
                   {'answer': answer, 'answer_id': answer_id})


@database_common.connection_handler
def add_comment(cursor, data):
    cursor.execute("""
                    INSERT INTO comment (question_id, answer_id, message, submission_time, edited_count)
                    VALUES (%s, %s, %s, %s, %s)
    """, (data.get('question_id'), data.get('answer_id'), data.get('message'),
          data.get('submission_time'), data.get('edited_count')))


@database_common.connection_handler
def get_all_comments(cursor):
    cursor.execute("""
                      SELECT * FROM comment
                      ORDER BY submission_time DESC
                    """)
    return cursor.fetchall()


@database_common.connection_handler
def get_password_by_username(cursor, user_name):
    cursor.execute("""
                    SELECT password FROM users
                    WHERE user_name LIKE %(user_name)s  
                    """,
                   {'user_name': user_name})
    return cursor.fetchone()


@database_common.connection_handler
def get_question_by_id(cursor, question_id):
    cursor.execute("""
                    SELECT * FROM question
                    WHERE id = %(question_id)s
                    ORDER BY submission_time DESC;
                    
    """, {'question_id': question_id})
    return cursor.fetchone()


@database_common.connection_handler
def get_answer_by_id(cursor, answer_id):
    cursor.execute("""
                    SELECT * FROM answer
                    WHERE id = %(answer_id)s
                    ORDER BY submission_time DESC;
    """, {'answer_id': answer_id})
    return cursor.fetchone()


@database_common.connection_handler
def add_new_user(cursor, user_data):
    cursor.execute("""
                    INSERT INTO users(user_name, password, registration_time)
                    VALUES (%s, %s, %s)
                    """, (user_data.get('user_name'), user_data.get('password'), user_data.get('registration_time')))


@database_common.connection_handler
def list_all_user(cursor):
    cursor.execute("""
                    SELECT user_name, registration_time FROM users
                    ORDER BY registration_time DESC
                    """)
    return cursor.fetchall()


@database_common.connection_handler
def get_id_by_user_name(cursor, user_name):
    cursor.execute("""
                    SELECT id FROM users
                    WHERE user_name= %(user_name)s;
    """, {'user_name': user_name})
    return cursor.fetchone()
