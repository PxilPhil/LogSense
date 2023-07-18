from flask import Flask, jsonify, request, Blueprint

import db_access

insert_data = Blueprint("insert_data", static_folder="../static", template_folder="../templates", import_name="insert_data")


@insert_data.route('/', methods=['POST'])
def injest_all_data():
    data = request.get_json()

    return jsonify({'error':'notimplementet yet'})