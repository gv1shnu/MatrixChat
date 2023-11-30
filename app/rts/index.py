# Third-party libraries
from flask import Blueprint, abort, render_template
from jinja2 import TemplateNotFound

# Internal imports
from utl.logger import Logger
from src.handler import handler
from decl import CURRENT_USER

index_bp = Blueprint('index', __name__)

logger = Logger()


# Home route of the application
@index_bp.route('/')
def index():
    try:
        messages = handler.get_all()
        try:
            return render_template(
                "index.html",
                messages=messages,
                current_user=CURRENT_USER
            )
        except TemplateNotFound:
            logger.error(f"index.html was not found.")
            abort(404)
    except Exception as e:
        logger.info(f"{str(e)}")
