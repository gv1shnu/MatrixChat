# Third-party libraries
from flask import Blueprint, abort, render_template
from jinja2 import TemplateNotFound

# Internal imports
from utl.logger import Logger

index_bp = Blueprint('index', __name__)

logger = Logger()


# Home route of the application
@index_bp.route('/')
def index():
    try:
        return render_template(
            "index.html"
        )
    except TemplateNotFound:
        logger.error(f"index.html was not found.")
        abort(404)
