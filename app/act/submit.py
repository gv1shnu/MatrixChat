# Third-party libraries
from flask import (
    Blueprint, request, redirect, url_for
)

# Internal imports
from decl import CURRENT_RECIPIENT
from src.handler import handler
from utl.logger import Logger

fetch_bp = Blueprint('fetch', __name__)
logger = Logger()


# submit route of the fetch blueprint
@fetch_bp.route(
    '/submit', methods=['POST']
)
def submit():
    # Fetch the POST requests from index route
    message: str = request.form.get('msg')
    handler.insert(receiver=CURRENT_RECIPIENT, message=message)
    return redirect(url_for('index.index'))
