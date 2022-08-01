from flask import (
        Blueprint
)

bp = Blueprint("hello", __name__, url_prefix="/hello")

@bp.route("/jerry", methods=["GET"])
def hello_jerry():
    return "Hello Jerry"

