# Flask blueprint for api routes
from flask import Blueprint, jsonify

from .llm import llm_bp
from .game import game_bp
from .database import database_bp
from .document import document_bp
from .auth.token import auth_bp
from .error import error_bp
from .auth.wrapper import require_token

api = Blueprint('api', __name__)
api.register_blueprint(llm_bp, url_prefix='/llm')
api.register_blueprint(game_bp, url_prefix='/game')
api.register_blueprint(database_bp, url_prefix='/database')
api.register_blueprint(document_bp, url_prefix='/document')
api.register_blueprint(auth_bp, url_prefix='/auth')
api.register_blueprint(error_bp)

@api.route('/', endpoint='api_home')
@require_token
def api_home():
    return jsonify({
        'message': 'Hello world!'
    })