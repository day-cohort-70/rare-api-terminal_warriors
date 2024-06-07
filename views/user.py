import sqlite3
import json
from datetime import datetime

def login_user(user):
    # Checks for the user in the database
    # Args:
    #     user (dict): Contains the username and password of the user trying to login
    # Returns:
    #     json string: If the user was found will return valid boolean of True and the user's id as the token
    #                  If the user was not found will return valid boolean False

    with sqlite3.connect('./db.sqlite3') as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
            select id, username
            from Users
            where username = ?
            and password = ?
        """, (user['username'], user['password']))

        user_from_db = db_cursor.fetchone()

        if user_from_db is not None:
            response = {
                'valid': True,
                'token': user_from_db['id']
            }
        else:
            response = {
                'valid': False
            }

        return json.dumps(response)


def create_user(user_request_body):

    with sqlite3.connect('./db.sqlite3') as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        Insert into Users (
            first_name, 
            last_name, 
            username, 
            email, 
            password, 
            bio, 
            created_on, 
            active
        ) 
        values (?, ?, ?, ?, ?, ?, ?, 1)
        """, (
            user_request_body['first_name'],
            user_request_body['last_name'],
            user_request_body['username'],
            user_request_body['email'],
            user_request_body['password'],
            user_request_body['bio'],
            datetime.now()
        ))

        id = db_cursor.lastrowid

        return json.dumps({
            'token': id,
            'valid': True
        })


def update_user(user, body):
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
            UPDATE Users
                SET
                    first_name = ?,
                    last_name = ?,
                    email = ?,
                    bio = ?,
                    username = ?,
                    password = ?,
                    profile_image_url = ?
            WHERE id = ?
            """,
            (body['first_name'], body['last_name'], body['email'], body['bio'], body['username'], body['password'], body['profile_image_url'], user)
        )

    updated_user = {
        "id": user,
        "first_name": body['first_name'],
        "last_name": body['last_name'],
        "email": body['email'],
        "bio": body['bio'],
        "username": body['username'],
        "profile_image_url":body['profile_image_url']
    }

    return json.dumps(updated_user)


def list_users(url):

    query_params = url['query_params']

    with sqlite3.connect('./db.sqlite3') as conn:
        conn.row_factory=sqlite3.Row
        db_cursor=conn.cursor()

        query_string = """
            SELECT
                *
            FROM Users
        """

        #check for query parameters
        if query_params:
            conditions = []
            parameters = []

            #look at each key/value pair and dynamically add each condition to SQL query (query_string)
            for key, values in query_params.items():

                conditions.append(f"{key} = ?")
                parameters.append(values[0])

            query_string += " WHERE " + " AND " .join(conditions)
            db_cursor.execute(query_string,(parameters))

        else:
            db_cursor.execute(query_string)

        #Write the SQL query to get the information you want

        query_results=db_cursor.fetchall()

        users=[]
        for row in query_results:
            users.append(dict(row))

        response_body = json.dumps(users)

    return response_body


def retrieve_user(pk):
    with sqlite3.connect('./db.sqlite3') as conn: 
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT u.id, u.first_name, u.last_name, u.username, u.email, u.bio, u.profile_image_url, u.created_on, u.active
        FROM Users u
        WHERE u.id = ?
        """, (pk,))

        user = db_cursor.fetchone()

    if user is None:
        return 'id not found'

    user_dictionary = dict(user)
    
    return json.dumps(user_dictionary)


def delete_user(pk):
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # write the SQL query to get the information you want
        db_cursor.execute(
            """
        DELETE FROM Users WHERE id = ?
                          
                          """,
            (pk,),
        )
        
        number_of_rows_delete = db_cursor.rowcount
    return True if number_of_rows_delete > 0 else False