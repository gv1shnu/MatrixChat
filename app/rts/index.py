# Third-party libraries
from flask import Blueprint, abort, render_template, session
from flask_login import current_user, login_required
from jinja2 import TemplateNotFound

# Internal imports
from utl.logger import Logger
from src.handler import handler

index_bp = Blueprint('index', __name__)
logger = Logger()


# Home route of the application
@index_bp.route('/')
@login_required
def index():
    try:
        user = session.get('CURRENT_USER')
        if not user:
            # Weird shit going on here
            email = current_user.name
            user = email.split('@')[0]
            session['CURRENT_RECIPIENT'] = session['CURRENT_USER'] = user
        messages = handler.get_all_messages_for(username=user)
        try:
            return render_template(
                "index.html",
                messages=messages,
                current_user=user
            )
        except TemplateNotFound:
            logger.error(f"index.html was not found.")
            abort(404)
    except Exception as e:
        logger.info(f"Error at index.py: {str(e)}")
