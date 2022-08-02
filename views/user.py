import json
from flask import (
        Blueprint, request, current_app, jsonify
)
from models.user import User

bp = Blueprint("user", __name__, url_prefix="/")

@bp.route("/signup", methods=["POST"])
def signup():
    body = json.loads(request.data)
    # if valid_user_json(body):
    new_user = User(name=body["name"], 
                    email=body["email"],
                    # TODO: hash this bad boi
                    password=body["password"])
    string_user = new_user.to_json()
    resp = jsonify(string_user)
    new_user.save()

    return resp

