import secrets
import string

def gen_salt():
    salt = ''
    for i in range(64):
        salt += ''.join(secrets.choice(string.ascii_letters + string.digits))
    return salt