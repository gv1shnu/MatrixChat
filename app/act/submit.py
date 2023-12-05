# Third-party libraries
from flask import (
    Blueprint, request, redirect, url_for, session
)
from flask_login import login_required

# Internal imports
from src.handler import handler
from utl.logger import Logger

fetch_bp = Blueprint('fetch', __name__)
logger = Logger()


def validate(message: str):
    if not message:
        raise ValueError("Empty message")
    pass


# submit route of the fetch blueprint
@fetch_bp.route(
    '/submit', methods=['POST']
)
@login_required
def submit():
    # Fetch the POST requests from index route
    message: str = request.form.get('msg')
    try:
        validate(message)
    except Exception as e:
        logger.error(f"Error here: {e}")

    recipient = session['CURRENT_RECIPIENT']

    # processing
    if message.startswith('@'):
        message = message.split(' ')[0]
        session['CURRENT_RECIPIENT'] = message[1:]
    elif message == "logout":
        return redirect(url_for('login.logout'))
    elif message == "to?":
        logger.debug(f"To {recipient}")
    elif message == "help":
        # Add instructions display functionality here
        pass
    else:
        user = session['CURRENT_USER']
        if recipient is not None:
            if user is not None:
                handler.insert(sender=user, receiver=recipient, message=message)
            else:
                logger.error("Invalid Sender")
        else:
            logger.error("Invalid Recipient")
    return redirect(url_for('index.index'))
