# Flask Blueprint for Database routes.
import json
from flask import Blueprint, request, jsonify
from ..models.llm import getModel
from ..database import mongo
from .auth.wrapper import require_token

database_bp = Blueprint('database', __name__)

@database_bp.route('/material', methods=['POST'])
@require_token
def get_material():
    """
    Get the material content from the database
    ---
    tags:
        - database
    consumes:
        - application/json
    parameters:
        - in: body
          name: body
          schema:
            required:
                - material_id
            properties:
                material_id:
                    type: string
            example:
                material_id: 6552b7cacdbae5d00cfcc7c4
    security:
        - ApiKeyAuth: []
    responses:
        200:
            description: Material Content
            schema:
                properties:
                    content:
                        type: string
                example:
                    content: "This is a sample text"
        400:
            description: Error message
            schema:
                type: object
                properties:
                    error:
                        type: string
        401:
            description: Token is missing
            schema:
                type: object
                properties:
                    error:
                        type: string
        403:
            description: Invalid token
            schema:
                type: object
                properties:
                    error:
                        type: string
    """
    data = request.get_json()

    if 'material_id' not in data:
        return jsonify({
            'error': 'material_id not provided'
        }), 400
    material_id = data['material_id']

    try:
        material = mongo.getMaterial(material_id)
    except:
        return jsonify({
            'error': 'error fetching material'
        }), 400
    
    if not material:
        return jsonify({
            'error': 'material not found'
        }), 400
    
    text, _, _ = material

    return jsonify({
        'content': text
    })

@database_bp.route('/game', methods=['POST'])
@require_token
def get_game():
    """
    Get the game from the database
    ---
    tags:
        - database
    consumes:
        - application/json
    parameters:
        - in: body
          name: body
          schema:
            required:
                - game_id
            properties:
                game_id:
                    type: string
            example:
                game_id: 6552ba84a316097da00c9aa5
    security:
        - ApiKeyAuth: []
    responses:
        200:
            description: Game Content
            schema:
                properties:
                    game:
                        type: object
                        properties:
                            content:
                                type: object
                            type:
                                type: string
                            material_id:
                                type: string
                example:
                    game: 
                        content: [{'A': 'To create efficient software solutions', 'Answer': 'C', 'B': 'To design user-friendly interfaces', 'C': 'To transform conceptual ideas into functional applications', 'D': 'To foster robust and reliable software', 'Question': 'What is the main goal of software development?'}, {'A': 'Agile methodologies', 'Answer': 'A', 'B': 'Waterfall methodologies', 'C': 'Scrum methodologies', 'D': 'Kanban methodologies', 'Question': 'Which methodology promotes flexibility and responsiveness in software development?'}]
                        type: "mcqs"
                        material_id: "6552b7cacdbae5d00cfcc7c4"
        400:
            description: Error message
            schema:
                type: object
                properties:
                    error:
                        type: string
        401:
            description: Token is missing
            schema:
                type: object
                properties:
                    error:
                        type: string
        403:
            description: Invalid token
            schema:
                type: object
                properties:
                    error:
                        type: string
    """
    data = request.get_json()

    if 'game_id' not in data:
        return jsonify({
            'error': 'game_id not provided'
        }), 400
    game_id = data['game_id']

    try:
        game = mongo.getGame(game_id)
    except:
        return jsonify({
            'error': 'error fetching game'
        }), 400
    
    if not game:
        return jsonify({
            'error': 'game not found'
        }), 400
    
    game_content, game_type, material_id = game

    try:
        game_content = json.loads(game_content)
    except:
        return jsonify({
            'error': 'error parsing game content'
        }), 400

    return jsonify({
        'game': {
            'content': game_content,
            'type': game_type,
            'material_id': str(material_id)
        }
    })