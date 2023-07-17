import secrets
import string

from flask import jsonify


def gen_salt():
    salt = ''
    for i in range(64):
        salt += ''.join(secrets.choice(string.ascii_letters + string.digits))
    return salt