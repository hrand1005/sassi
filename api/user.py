import json
from flask import (
    Blueprint, request, current_app, jsonify
)
from flask_expects_json import expects_json
from models.user import User

bp = Blueprint("user", __name__, url_prefix="/")

user_schema = {
    "title": "user",
    "type": "object",
    "properties": {
        "id": {
            "type": "integer",
            "exlusiveMinimum": "1"
        },
        "name": {
            "type": "string",
            "minLength": 3,
            "maxLength": 20
        },
        "email": {
            "type": "string",
            "pattern": "^\S+@\S+$" # simplest email regex
        },
        "password": {
            "type": "string",
            "minLength": 5
        },
    },
    # TODO: Add Required Keys
}

@bp.route("/signup", methods=["POST"])
@expects_json(user_schema)
def signup():
    user_json = request.json

    ### db or repository operation ###
    new_user = User(name=user_json["name"], 
                    email=user_json["email"],
                    # TODO: hash this bad boi
                    password=user_json["password"])
    new_user.save()

    # could use transformer here
    string_user = new_user.to_json() 
    return jsonify(string_user)

