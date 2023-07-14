from flask import Blueprint, Flask, request, jsonify
import psycopg2
from psycopg2 import extras
import configparser
import logging

from api.user import user

app = Flask(__name__)

app.register_blueprint(user, url_prefix="/user")

if __name__ == '__main__':
    app.run(debug=True)
