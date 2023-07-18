from flask import Flask, jsonify, request, Blueprint

import db_access
from db_access.pc import get_pcs_by_userid, get_pcs

pc = Blueprint("pc", static_folder="../static", template_folder="../templates", import_name="pc")


@pc.route('/', methods=['GET'])
def get_all_pcs():
    return jsonify({'pcs': db_access.pc.get_pcs()})


@pc.route('/user/<user_id>', methods=['GET'])
def get_pc_by_user_id(user_id):
    return jsonify({'pcs': db_access.pc.get_pcs_by_userid(user_id)}), 201


@pc.route('/add_pc', methods=['POST'])
def add_pc_api():
    data = request.get_json()
    user_id = data.get('user_id')
    hardware_uuid = data.get('hardware_uuid')
    client_name = data.get('client_name')

    pc_id = db_access.pc.add_pc(user_id, hardware_uuid, client_name)
    if pc_id == -1:
        return jsonify({'error': 'Failed to insert pc.'}), 500

    return jsonify({'pc_id': pc_id}), 201
