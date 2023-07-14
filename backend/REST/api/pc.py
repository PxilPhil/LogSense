from flask import Flask, jsonify, request, Blueprint
import random
import string
import secrets
import hashlib

import api.helper
import db_access.pc
from api.helper import gen_salt
from db_access.user import IdentifierType, add_user, check_login

pc = Blueprint("pc", static_folder="../static", template_folder="../templates", import_name="pc")


@pc.route('/', methods=['GET'])
def get_all_pcs():
    return jsonify(db_access.pc.get_pcs())


@pc.route('/add_pc', methods=['POST'])
def add_pc_api():
    data = request.get_json()
    user_id = data.get('user_id')
    hardware_uuid = data.get('hardware_uuid')
    client_name = data.get('clientName')

    pc_id = db_access.pc.add_pc(user_id, hardware_uuid, client_name)
    if pc_id == -1:
        return jsonify({'error': 'Failed to insert pc.'}), 500

    return jsonify({'pc_id': pc_id}), 201

