import hashlib
import re


def is_valid_email(email: str):
    email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(email_pattern, email) is not None

def hash_password(pwd, salt):
    return str(hashlib.sha256((str(salt) + str(pwd)).encode()).hexdigest())