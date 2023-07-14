from flask import Flask, jsonify, request, Blueprint
import random
import string
import secrets
import hashlib

import api.helper
import db_access.user
from api.helper import gen_salt
from db_access.user import IdentifierType, add_user, check_login

user = Blueprint("user", static_folder="../static", template_folder="../templates", import_name="user")


@user.route('/', methods=['GET'])
def get_all_users():
    return jsonify(db_access.user.get_users())


@user.route('/check_login', methods=['POST'])
def check_login_api():
    data = request.get_json()
    email = data.get('email')
    user_id = data.get('id')
    name = data.get('name')
    password = data.get('password')

    # Query the database to check if the login credentials are valid
    # Replace the code below with your database query
    if email:
        valid_login = check_login(email, IdentifierType.EMAIL, password)
    elif user_id:
        valid_login = check_login(user_id, IdentifierType.ID, password)
    elif name:
        valid_login = check_login(name, IdentifierType.NAME, password)
    else:
        return jsonify({'error': 'Invalid request'}), 400

    return jsonify({'valid_login': valid_login})


@user.route('/add_user', methods=['POST'])
def add_user_api():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    salt = api.helper.gen_salt()

    user_id = db_access.user.add_user(name, email, password, salt)
    if user_id == -1:
        return jsonify({'error': 'Failed to insert user.'}), 500

    return jsonify({'user_id': user_id}), 201



