# Third-party libraries
from flask import (
    Blueprint,
    abort,
    render_template,
    session,
    request,
    jsonify
)
from flask_login import current_user, login_required
from jinja2 import TemplateNotFound

# Internal imports
from decl import INDEX_TEMPLATE, INSTRUCTIONS
from utl.logger import Logger
from src.handler import handler, USER_LIST

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

        recipient = session.get('CURRENT_RECIPIENT')
        messages = handler.get_all_messages_for(
            username=user
        )
        try:
            return render_template(
                INDEX_TEMPLATE,
                messages=messages,
                current_user=user,
                current_recipient=recipient,
                instructions=INSTRUCTIONS
            )
        except TemplateNotFound:
            logger.error(
                f"{INDEX_TEMPLATE} was not found."
            )
            abort(404)
    except Exception as e:
        logger.info(
            f"Error at index.py: {str(e)}"
        )


@index_bp.route(
    '/get_users',
    methods=['GET']
)
def get_users():
    search_term = request.args.get('term', '')[1:]
    results = [
        "@" + word
        for word in USER_LIST
        if search_term.lower() in word.lower()
    ]
    return jsonify(results)
