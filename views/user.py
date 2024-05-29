#user.py
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

def list_users():
    """Lists all users"""
    with sqlite3.connect('./db.sqlite3') as conn:
        conn.row_factory=sqlite3.Row
        db_cursor=conn.cursor()

        #Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
                          u.id,
                          u.first_name,
                          u.last_name,
                          u.username,
                          u.email,
                          u.bio,
                          u.password,
                          u.profile_image_url,
                          u.created_on,
                          u.active

            FROM Users u
            """)
        query_results=db_cursor.fetchall()

        users=[]
        for row in query_results:
            users.append(dict(row))

        serialized_users=json.dumps(users)

    return serialized_users
        
    
def retrieve_user(pk):
    """Retrieves a single user by primary key"""
    with sqlite3.connect('./db.sqlite3') as conn: 
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT u.id, u.first_name, u.last_name, u.username, u.email, u.bio, u.profile_image_url, u.created_on, u.active
        FROM Users u
        WHERE u.id = ?
        """, (pk,))
        
        user = db_cursor.fetchone()
        dictionary_version_of_object = dict(user) if user else {}
        serialized_user = json.dumps(dictionary_version_of_object)

    return serialized_user
