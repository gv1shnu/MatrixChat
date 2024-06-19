# Third-party libraries
from flask import (
    Blueprint,
    request,
    redirect,
    url_for,
    session
)
from flask_login import login_required

# Internal imports
from src.handler import handler, USER_LIST
from utl.logger import Logger

fetch_bp = Blueprint('fetch', __name__)
logger = Logger()


def validate(message: str):
    if not message:
        raise ValueError("Empty message")
    pass


# submit route of the fetch blueprint
@fetch_bp.route(
    '/submit',
    methods=['POST']
)
@login_required
def submit():
    # Fetch the POST requests from index route
    message: str = request.form.get('msg')
    try:
        validate(message)
    except Exception as e:
        logger.error(f"Error here: {e}")

    recipient = session.get('CURRENT_RECIPIENT')

    # processing
    if message.startswith('@'):
        message = message.split(' ')[0]
        user_ = message[1:]
        if user_ in USER_LIST:
            session['CURRENT_RECIPIENT'] = user_
        else:
            logger.debug("Invalid Recipient")
    elif message == "logout":
        return redirect(url_for('login.logout'))
    elif message == "to?":
        recipient = session['CURRENT_RECIPIENT']
        logger.debug(f"To {recipient}")
    else:
        user = session.get('CURRENT_USER')
        if recipient is not None:
            if user is not None:
                handler.insert(
                    sender=user,
                    receiver=recipient,
                    message=message
                )
            else:
                logger.error("Invalid Sender")
        else:
            logger.error("Invalid Recipient")
    return redirect(url_for('index.index'))
