from flask import Blueprint, Flask, request, jsonify

from api.user import user
from api.pc import pc

app = Flask(__name__)

app.register_blueprint(user, url_prefix="/user")
app.register_blueprint(pc, url_prefix="/pc")

if __name__ == '__main__':
    app.run(debug=True)
