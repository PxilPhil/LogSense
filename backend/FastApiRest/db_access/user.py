import logging
import hashlib

import psycopg2
from psycopg2 import errorcodes

from db_access import conn_pool
from db_access.helper import is_valid_email, hash_password
from exceptions.DataBaseExcepion import DataBaseException
from exceptions.WrongLoginException import WrongLoginException
from exceptions.InvalidParametersException import InvalidParametersException
from model.data import AlertData

logging.basicConfig(filename='app.log', level=logging.INFO)


class IdentifierType:
    EMAIL = 'email'
    NAME = 'name'
    ID = 'id'


def get_salt(identifier, identifier_type):
    conn = conn_pool.getconn()
    cursor = conn.cursor()
    try:
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
    except psycopg2.DatabaseError as e:
        raise DataBaseException()
    finally:
        conn_pool.putconn(conn)


def check_login(identifier, identifier_type, password):
    conn = conn_pool.getconn()
    cursor = conn.cursor()
    try:
        if identifier_type == IdentifierType.EMAIL:
            query = "SELECT password_hash, ID FROM logSenseUser WHERE EMail = %s;"
        elif identifier_type == IdentifierType.NAME:
            query = "SELECT password_hash, ID FROM logSenseUser WHERE Name = %s;"
        elif identifier_type == IdentifierType.ID:
            query = "SELECT password_hash, ID FROM logSenseUser WHERE ID = %s;"
        else:
            raise InvalidParametersException()

        params = (identifier,)

        cursor.execute(query, params)
        result = cursor.fetchone()

        if result:
            stored_password_hash, user_id = result
            hashed_password = hash_password(password, get_salt(identifier, identifier_type))
            return hashed_password == stored_password_hash, user_id
        else:
            raise WrongLoginException()
    except psycopg2.DatabaseError as e:
        raise DataBaseException()
    finally:
        conn_pool.putconn(conn)


def add_user(name, email, password, salt):
    if not is_valid_email(email):
        raise InvalidParametersException(detail="Invalid email")

    # Hash the provided password using the salt
    hashed_password = hash_password(password, salt)

    # Insert the new user into the database
    query = "INSERT INTO logSenseUser (Name, EMail, password_hash, Salt) VALUES (%s, %s, %s, %s) RETURNING ID;"
    params = (str(name), str(email), str(hashed_password), str(salt))

    user_id = -1

    conn = conn_pool.getconn()
    cursor = conn.cursor()
    try:
        cursor.execute(query, params)
        user_id = cursor.fetchone()[0]
        print("Insertion successful. User ID:", user_id)

        conn.commit()
    except psycopg2.DatabaseError as e:
        conn.rollback()
        if e.pgcode == psycopg2.errorcodes.UNIQUE_VIOLATION:
            raise InvalidParametersException(detail="Email or Name already exists.")
        raise DataBaseException(detail="User Could not be inserted")
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn_pool.putconn(conn)

    return user_id


def get_users():
    conn = conn_pool.getconn()
    cursor = conn.cursor()
    try:
        query = """
                SELECT Name FROM logsenseuser
                """
        cursor.execute(query)
        rows = cursor.fetchall()

        users = []
        for row in rows:
            user = {'name': row[0]}
            users.append(user)
        return users
    except psycopg2.DatabaseError as e:
        raise DataBaseException()
    finally:
        conn_pool.putconn(conn)


def get_all_user_alerts(user_id, start, end):  # gets all alerts per user between a start and end date
    conn = conn_pool.getconn()
    cursor = conn.cursor()
    try:
        get_user_anomalies_query = """
        SELECT a.type, a.severity_level, a.message, aa.change_in_percentage, ad.name, ad.measurement_time, aa.pc_id
        FROM applicationdata_anomaly aa
        INNER JOIN applicationdata ad ON aa.applicationdata_id = ad.id
        INNER JOIN anomaly a ON a.id = aa.anomaly_id
        WHERE ad.measurement_time BETWEEN %s AND %s
        AND aa.user_id = %s;
        """
        cursor.execute(get_user_anomalies_query, (start, end, user_id))
        result = cursor.fetchall()

        alert_list = []
        if result:
            for row in result:
                alert = AlertData(
                    type=row[0],
                    severity_level=row[1],
                    message=row[2],
                    change_in_percentage=row[3],
                    name=row[4],
                    measurement_time=row[5],
                    pc_id=row[6],
                )
                alert_list.append(alert)

        return alert_list
    except psycopg2.DatabaseError as e:
        raise DataBaseException()
    finally:
        conn_pool.putconn(conn)
