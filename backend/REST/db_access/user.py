import logging
import hashlib

from db_access import cursor, conn
from db_access.helper import is_valid_email

logging.basicConfig(filename='app.log', level=logging.INFO)


class IdentifierType:
    EMAIL = 'email'
    NAME = 'name'
    ID = 'id'


def get_salt(identifier, identifier_type):
    if identifier_type == IdentifierType.EMAIL:
        query = "SELECT Salt FROM logSenseUser WHERE EMail = %s;"
    elif identifier_type == IdentifierType.NAME:
        query = "SELECT Salt FROM logSenseUser WHERE Name = %s;"
    elif identifier_type == IdentifierType.ID:
        query = "SELECT Salt FROM logSenseUser WHERE ID = %s;"
    else:
        return None

    params = (identifier,)

    cursor.execute(query, params)
    salt = cursor.fetchone()

    if salt:
        return salt[0]  # Assuming salt is the first column in the query result
    else:
        return None


def check_login(identifier, identifier_type, password):
    if identifier_type == IdentifierType.EMAIL:
        query = "SELECT PasswordHash FROM logSenseUser WHERE EMail = %s;"
    elif identifier_type == IdentifierType.NAME:
        query = "SELECT PasswordHash FROM logSenseUser WHERE Name = %s;"
    elif identifier_type == IdentifierType.ID:
        query = "SELECT PasswordHash FROM logSenseUser WHERE ID = %s;"
    else:
        return False

    params = (identifier,)

    cursor.execute(query, params)
    stored_password_hash = cursor.fetchone()

    if stored_password_hash:
        hashed_password = str(hashlib.sha256(
            (str(get_salt(identifier, identifier_type)) + str(password)).encode()
        ).hexdigest())
        return hashed_password == stored_password_hash[0]
    else:
        return False


def add_user(name, email, password, salt):
    if not is_valid_email(email):
        raise ValueError("Invalid email")

    # Hash the provided password using the salt
    hashed_password = str(hashlib.sha256((str(salt) + str(password)).encode()).hexdigest())

    # Insert the new user into the database
    query = "INSERT INTO logSenseUser (Name, EMail, PasswordHash, Salt) VALUES (%s, %s, %s, %s) RETURNING ID;"
    params = (str(name), str(email), str(hashed_password), str(salt))

    user_id = -1
    try:
        cursor.execute(query, params)
        user_id = cursor.fetchone()[0]
        print("Insertion successful. User ID:", user_id)
    except Exception as e:
        print("Error occurred:", str(e))

    conn.commit()

    return user_id


def get_users():
    query = """
            SELECT Name FROM logsenseuser
            """
    cursor.execute(query)
    rows = cursor.fetchall()

    users = []
    for row in rows:
        user = row[0]
        users.append(user)
    return users
