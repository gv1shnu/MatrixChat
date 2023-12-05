# Third-party libraries
from flask import Blueprint, redirect, url_for, request, render_template, abort, session
from flask_login import login_user, login_required, logout_user
from jinja2 import TemplateNotFound

# Internal imports
from utl.logger import Logger
from utl.auth import google_callback, login_user_with_google
from src.user import User

login_bp = Blueprint('login', __name__)
logger = Logger()


@login_bp.route('/unauth')
def unauth():
    try:
        return render_template(
            "login.html"
        )
    except TemplateNotFound:
        logger.error(f"index.html was not found.")
        abort(404)


@login_bp.route("/login")
def auth():
    # Call the login_user_with_google function to get the Google login URL
    google_login_url = login_user_with_google()
    return redirect(google_login_url)


@login_bp.route("/login/callback")
def callback():
    # Call the callback function to handle Google's callback and user authentication
    user: User = google_callback(request)
    login_user(user)
    return redirect(
        url_for("index.index")
    )


@login_bp.route("/logout")
@login_required
def logout():
    session.clear()
    logout_user()
    return redirect(url_for("index.index"))
