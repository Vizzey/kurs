from flask import Blueprint

# Blueprint for authentication-related routes
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

# Register view handlers
from . import views  # noqa: E402,F401

# Re-export commonly used helpers
from .utils import login_required, permission_required, current_user  # noqa: E402,F401

__all__ = ['auth_bp', 'login_required', 'permission_required', 'current_user']
