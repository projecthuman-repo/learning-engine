from flask import request, jsonify
from ...database.mongo import verifyToken

def require_token(func):
    def wrapper(*args, **kwargs):
        api_key = request.headers.get('token')
        if not api_key:
            return jsonify({'error': 'Token is missing'}), 401
        if not verifyToken(api_key):
            return jsonify({'error': 'Invalid Token'}), 403
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    wrapper.__doc__ = func.__doc__
    return wrapper