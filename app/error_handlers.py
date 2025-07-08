from flask import Blueprint
from app.routes.utils.responses import error_response

errors_bp = Blueprint('errors', __name__)


@errors_bp.app_errorhandler(404)
def not_found(error):
    return error_response(f"Endpoint not found, Error: {error}", 404)


@errors_bp.app_errorhandler(405)
def method_not_allowed(error):
    return error_response(f"Method not allowed, Error: {error}", 405)


@errors_bp.app_errorhandler(500)
def internal_error(error):
    return error_response(f"Internal server error, Error: {error}", 500)
