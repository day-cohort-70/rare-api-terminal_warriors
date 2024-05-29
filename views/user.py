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
    # Adds a user to the database when they register
    # Args:
    #     user (dictionary): The dictionary passed to the register post request
    # Returns:
    #     json string: Contains the token of the newly created user

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
        rows_affected = db_cursor.rowcount
    return True if rows_affected > 0 else False