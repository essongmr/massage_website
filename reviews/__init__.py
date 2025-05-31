from flask import Blueprint

reviews_bp = Blueprint(
    'reviews',
    __name__,
    url_prefix='/reviews',
    template_folder='templates'
)

from . import routes
