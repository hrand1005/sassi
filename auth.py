import functools
import re
from flask import (
    Blueprint, flash, g, session, redirect, render_template, request, url_for
)
from models.user import User
from werkzeug.security import check_password_hash, generate_password_hash

# username and password constraints
USERNAME_MIN_LENGTH = 3
PASSWORD_MIN_LENGTH = 5
EMAIL_MIN_LENGTH = 6

# html templates
SIGNUP_HTML = "auth/signup.html"
LOGIN_HTML = "auth/login.html"

bp = Blueprint("auth", __name__, url_prefix="/")

@bp.before_app_request
def load_session():
    user_id = session.get("user_id")
    if user_id:
        g.user = User.objects(pk=user_id).first()
    else:
        g.user = None



@bp.route("/login", methods=["GET"])
def render_login():
    """
    Renders the login page.
    """
    return render_template(LOGIN_HTML)

@bp.route("/login", methods=["POST"])
def submit_login():
    """
    Attmepts to log in an existing user from the provided email and password.
    If the user is found, the session's user_id field is set.
    """
    email = request.form.get("email")
    password = request.form.get("password")

    user = User.objects(email__iexact=email).first()
    if not user:
        flash(f"No user with email '{email}' exists.")
        return render_login()
    
    if not check_password_hash(user.password, password):
        flash(f"Incorrect password.")
        return render_login()

    session.clear()
    session["user_id"] = str(user.id)
    return redirect(url_for("index"))
    
@bp.route("/logout", methods=["GET"])
def logout():
    session.clear()
    return redirect(url_for('index'))

@bp.route("/signup", methods=["GET"])
def render_signup():
    """
    Renders the signup page.
    """
    return render_template(SIGNUP_HTML)

@bp.route("/signup", methods=["POST"])
def submit_signup():
    """
    Attempts to register a new user from the provided username and password.
    Checks that the provided fields meet requirements before creating a user.
    """
    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")

    try:
        check_username(username)
        check_email(email)
        check_password(password)
    except ValueError as e:
        flash(e)
        return render_signup()
    
    if User.objects(email__iexact=email).first():
        flash("A user with this email already exists.")
        return render_signup()

    try:
        User(name=username,
             email=email,
             password=generate_password_hash(password)).save()
    except Exception as e:
        flash(f"Catastrophic failure: {e}")

    return redirect(url_for("auth.render_login"))

def check_username(username: str):
    """
    Raises error iff the provided username doesn't meet the length requirements.
    """
    if username is None:
        raise ValueError("Username required.")
    if len(username) < USERNAME_MIN_LENGTH:
        raise ValueError(f"Username must be at least {USERNAME_MIN_LENGTH} characters.")
    # etc...
    return 

def check_password(password: str):
    """
    Raises error iff the provided password doesn't meet length and character requirements.
    """
    if password is None:
        raise ValueError("Password required.")
    if len(password) < PASSWORD_MIN_LENGTH:
        raise ValueError(f"Password must be at least {PASSWORD_MIN_LENGTH} characters.")
    # etc...
    return

def check_email(email: str):
    """
    Raises error iff the provided email doesn't match email regex.
    """
    if email is None:
        raise ValueError("Email required.")
    match = re.match("^\S+@\S+$", email)
    if not match or len(email) < EMAIL_MIN_LENGTH:
        raise ValueError(f"Invalid email field.")
    return

def authentication_required(view):
    @functools.wraps(view)
    def wrapped_view(*args, **kwargs):
        if g.user is None:
            return redirect(url_for("auth.render_login"))

        return view(*args, **kwargs)

    return wrapped_view

