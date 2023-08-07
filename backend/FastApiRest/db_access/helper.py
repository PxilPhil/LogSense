import hashlib
import re

import psycopg2

from db_access import conn_pool
from exceptions.NotFoundExcepion import NotFoundException
from exceptions.DataBaseExcepion import DataBaseException


def is_valid_email(email: str):
    email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(email_pattern, email) is not None


def hash_password(pwd, salt):
    return str(hashlib.sha256((str(salt) + str(pwd)).encode()).hexdigest())


def get_pcid_by_stateid(state_id: int):
    conn = conn_pool.getconn()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT pc_id FROM PCState WHERE id = %s", (state_id,))
        result = cursor.fetchone()

        if result:
            pc_id = result[0]
            return pc_id
        else:
            raise NotFoundException(detail=f"PC not found with StateID {str(state_id)}")
    except psycopg2.DatabaseError as e:
        raise DataBaseException()
    finally:
        conn_pool.putconn(conn)

def get_stateid_and_pcid_by_uuid(uuid: str):
    conn = conn_pool.getconn()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id, pc_id FROM PCState WHERE pc_id = (SELECT id FROM PC WHERE hardware_UUID = %s)",
                           (uuid,))
        ids = cursor.fetchone()

        if ids:
            #       state_id    , pc_id
            return ids[0], ids[1]
        else:
            return None
    except psycopg2.DatabaseError as e:
        raise DataBaseException()
    finally:
        conn_pool.putconn(conn)