# Flask Blueprint to handle errors
from flask import Blueprint, jsonify

error_bp = Blueprint('error', __name__)

@error_bp.app_errorhandler(404)
def not_found(error):
    return jsonify({
        'error': str(error)
    }), 404

@error_bp.app_errorhandler(405)
def method_not_allowed():
    return jsonify({
        'error': "Method not allowed"
    }), 405

@error_bp.app_errorhandler(500)
def internal_server_error(error):
    return jsonify({
        'error': str(error)
    }), 500

@error_bp.app_errorhandler(501)
def not_implemented(error):
    return jsonify({
        'error': str(error)
    }), 501

@error_bp.app_errorhandler(502)
def bad_gateway(error):
    return jsonify({
        'error': str(error)
    }), 502

@error_bp.app_errorhandler(503)
def service_unavailable(error):
    return jsonify({
        'error':error
    }), 503

@error_bp.app_errorhandler(504)
def gateway_timeout(error):
    return jsonify({
        'error': str(error)
    }), 504

@error_bp.app_errorhandler(505)
def http_version_not_supported(error):
    return jsonify({
        'error': str(error)
    }), 505