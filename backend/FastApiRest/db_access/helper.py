import hashlib
import re

from db_access import cursor


def is_valid_email(email: str):
    email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(email_pattern, email) is not None


def hash_password(pwd, salt):
    return str(hashlib.sha256((str(salt) + str(pwd)).encode()).hexdigest())


def get_pcid_by_stateid(state_id: int):
    cursor.execute("SELECT pc_id FROM PCState WHERE id = %s", (state_id,))
    result = cursor.fetchone()

    if result:
        pc_id = result[0]
        return pc_id
    else:
        return None

def get_stateid_and_pcid_by_uuid(uuid: str):
    cursor.execute("SELECT id, pc_id FROM PCState WHERE pc_id = (SELECT id FROM PC WHERE hardware_UUID = %s)",
                       (uuid,))
    pcstate_id = cursor.fetchone()

    if pcstate_id:
        #       state_id    , pc_id
        return pcstate_id[0], pcstate_id[1]
    else:
        return None