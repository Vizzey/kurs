import os
from flask import Blueprint
from models.sql_provider import SQLProvider

query_bp = Blueprint('query', __name__, url_prefix='/query')
provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))

from . import views  # noqa: E402,F401
