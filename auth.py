import json
from flask import (
    Blueprint, flash, redirect, render_template, request, url_for
)
from models.user import User
from werkzeug.security import check_password_hash, generate_password_hash

# username and password constraints
USERNAME_MIN_LENGTH = 3
PASSWORD_MIN_LENGTH = 5

bp = Blueprint("user", __name__, url_prefix="/")

@bp.route("/signup", methods=["GET"])
def render_signup():
    return render_template("auth/signup.html")

@bp.route("/signup", methods=["POST"])
def submit_signup():
    """
    Attempts to register a new user from the provided username and password.
    Checks that the provided fields meet requirements before creating a user.
    """
    username = request.form.get("username")
    password = request.form.get("password")

    try:
        check_username(username)
        check_password(password)
    except ValueError as e:
        flash(e)
        return render_signup()
    
    # TODO: enforce some unique characteristic
    new_user = User(name=username, password=generate_password_hash(password))
    new_user.save()

    return redirect(url_for("user.render_login"))

def check_username(username: str):
    """
    Raises error iff the provided username doesn't meet the length requirements.
    """
    if len(username) < USERNAME_MIN_LENGTH:
        raise ValueError(f"Username must be at least {USERNAME_MIN_LENGTH} characters.")
    # etc...
    return 

def check_password(password: str):
    """
    Raises error iff the provided password doesn't meet length and character requirements.
    """
    if len(password) < PASSWORD_MIN_LENGTH:
        raise ValueError(f"Password must be at least {PASSWORD_MIN_LENGTH} characters.")
    # etc...
    return

@bp.route("/login", methods=["GET"])
def render_login():
    return "hi mom"
