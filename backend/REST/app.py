from flask import Blueprint, Flask, request, jsonify

from api.insert import insert_data
from api.user import user
from api.pc import pc

app = Flask(__name__)

app.register_blueprint(user, url_prefix="/user")
app.register_blueprint(pc, url_prefix="/pc")
app.register_blueprint(insert_data, url_prefix="/insert_data")

if __name__ == '__main__':
    app.run(debug=True)
