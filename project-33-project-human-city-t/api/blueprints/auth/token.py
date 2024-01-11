from flask import request, jsonify
from flask import Blueprint, request, jsonify
from ...database.mongo import generateToken, checkUsername, isAdmin, checkPassword


auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/gettoken', methods=['POST'])
def get_token():
    """
    Get a token for a user
    ---
    tags:
        - auth
    consumes:
        - application/json
    parameters:
        - in: body
          name: body
          schema:
            required:
                - username
                - password
            properties:
                username:
                    type: string
                password:
                    type: string
            example:
                username: test
                password: test
    responses:
        200:
            description: Token generated
            schema:
                type: object
                properties:
                    token:
                        type: string
                example:
                    token: 1234567890   
        400:
            description: Error message
            schema:
                type: object
                properties:
                    error:
                        type: string
        500:
            description: Database connection error
            schema:
                type: object
                properties:
                    error:
                        type: string
    """
    username = request.json.get('username')
    password = request.json.get('password')

    if username is None or password is None:
        return jsonify({
            'error': 'Missing username or password'
        }), 400

    try:
        valid_username = checkUsername(username)
        valid_password = checkPassword(username, password) if valid_username else None
    except:
        return jsonify({
            'error': 'Database connection error'
        }), 500
    
    if not valid_username or not valid_password:
        return jsonify({
            'error': 'Invalid username or password'
        }), 400
    
    try:
        is_eligible = isAdmin(username)
    except:
        return jsonify({
            'error': 'Database connection error'
        }), 500
    
    if not is_eligible:
        return jsonify({
            'error': 'User not eligible to gain a token'
        }), 400
    
    try:
        token = generateToken(username)
    except:
        return jsonify({
            'error': 'Token generation error'
        }), 500
    
    return jsonify({
        'token': token
    }), 200