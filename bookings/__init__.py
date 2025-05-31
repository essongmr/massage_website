from flask import Blueprint

bookings_bp = Blueprint(
    'bookings',
    __name__,
    url_prefix='/',
    template_folder='templates'
)

from . import routes
