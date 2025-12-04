from flask import Blueprint

reports_bp = Blueprint('reports', __name__, url_prefix='/reports')

from . import views  # noqa: E402,F401

__all__ = ['reports_bp']
