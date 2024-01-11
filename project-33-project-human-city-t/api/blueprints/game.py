# Flask blueprint for game routes
import json
from flask import Blueprint, request, jsonify
from ..models.games import generate_crossword, generate_wordsearch
from ..database import mongo
from .auth.wrapper import require_token

game_bp = Blueprint('game', __name__)

@game_bp.route('/crossword', methods=['POST'])
@require_token
def get_crossword():
    """
    Generate a crossword puzzle
    ---
    tags:
        - game
    consumes:
        - application/json
    parameters:
        - in: body
          name: body
          schema:
            required:
                - game_id
                - grid_size
            properties:
                game_id:
                    type: string
                grid_size:
                    type: integer
            example:
                game_id: 6552ba84a316097da00c9aa5
                grid_size: 20
    security:
        - ApiKeyAuth: []
    responses:
        200:
            description: A crossword puzzle
            schema:
                properties:
                    crossword:
                        type: object
                        grid:
                            type: array
                            items:
                                type: array
                                items:
                                    type: string
                        hints:
                            type: object
                            properties:
                                horizontal:
                                    type: array
                                    items:
                                        type: object
                                        properties:
                                            number:
                                                type: integer
                                            hint:
                                                type: string
                                vertical:
                                    type: array
                                    items:
                                        type: object
                                        properties:
                                            number:
                                                type: integer
                                            hint:
                                                type: string
                    game_id:
                        type: string
                example:
                    crossword: {
                        grid: [
                            ['', '', '', '', 1, ' ', 2, ' ', ' ', ' ', '', '', '', '', '', 3, '', '', '', ''],
                            ['', '', '', '', '', '', ' ', '', '', '', '', '', '', '', '', ' ', '', '', '', ''],
                            ['', '', '', '', '', '', ' ', '', '', '', '', '', 4, ' ', ' ', ' ', ' ', ' ', ' ', ''],
                            ['', '', '', '', '', '', ' ', '', '', '', 5, '', '', '', '', ' ', '', '', '', ''],
                            ['', '', '', '', '', '', ' ', '', '', '', ' ', '', '', '', '', ' ', '', '', '', ''],
                            ['', '', '', '', '', '', ' ', '', '', '', ' ', '', '', 6, ' ', ' ', ' ', ' ', '', ''],
                            ['', '', '', '', '', '', ' ', '', '', '', ' ', '', '', '', '', ' ', '', '', '', ''],
                            ['', '', '', '', '', '', ' ', '', '', '', ' ', '', '', 7, '', ' ', '', '', '', ''],
                            ['', '', '', 8, '', 9, ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '', '', ''],
                            ['', '', '', ' ', '', '', ' ', '', '', '', ' ', '', '', ' ', '', ' ', '', '', '', ''],
                            ['', '', '', ' ', '', '', ' ', '', '', '', ' ', '', '', ' ', '', ' ', '', '', '', ''],
                            ['', '', '', ' ', '', '', '', '', '', '', ' ', '', '', ' ', '', ' ', '', '', '', ''],
                            ['', '', '', ' ', '', '', '', '', '', '', ' ', '', '', ' ', '', '', '', '', 10, ''],
                            ['', '', '', ' ', '', '', '', '', '', '', ' ', '', '', ' ', '', '', '', '', ' ', ''],
                            ['', '', '', ' ', '', '', '', '', '', '', '', '', '', ' ', '', '', '', '', ' ', ''],
                            ['', '', '', ' ', '', '', '', '', '', 11, ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ''],
                            ['', '', '', ' ', '', '', '', '', '', '', '', '', '', ' ', '', '', '', '', ' ', ''],
                            ['', '', '', 12, ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '', '', ' ', ''],
                            ['', '', '', ' ', '', '', '', '', '', '', '', '', '', ' ', '', '', '', '', ' ', ''],
                            ['', '', '', '', '', '', '', '', '', '', '', '', '', ' ', '', '', '', '', ' ', '']
                        ],
                        hints: {
                            "horizontal": [
                                {
                                    "hint": "The protection of computer systems from theft or damage.",
                                    "number": 12
                                },
                                {
                                    "hint": "A description of what a software should do.",
                                    "number": 9
                                },
                                {
                                    "hint": "The process of making software available for use.",
                                    "number": 11
                                },
                                {
                                    "hint": "The process of evaluating software to find bugs.",
                                    "number": 4
                                },
                                {
                                    "hint": "The process of writing instructions for a computer.",
                                    "number": 1
                                },
                                {
                                    "hint": "A set of principles for software development.",
                                    "number": 6
                                }
                            ],
                            "vertical": [
                                {
                                    "hint": "A system of practices, techniques, procedures, and rules.",
                                    "number": 7
                                },
                                {
                                    "hint": "The process of making software better.",
                                    "number": 3
                                },
                                {
                                    "hint": "The process of writing and maintaining the source code.",
                                    "number": 2
                                },
                                {
                                    "hint": "The process of modifying software after delivery.",
                                    "number": 8
                                },
                                {
                                    "hint": "The process of combining software components.",
                                    "number": 5
                                },
                                {
                                    "hint": "A set of instructions that tells a computer what to do.",
                                    "number": 10
                                }
                            ]
                        }
                    }
                    game_id: 6552b7cacdbae5d00cfcc7c4

        400:
            description: Bad request
            schema:
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

    if 'grid_size' not in data:
        return jsonify({
            'error': 'grid_size not provided'
        }), 400
    grid_size = data['grid_size']

    try:
        word_definitions_game = mongo.getGame(game_id)
    except:
        return jsonify({
            'error': "error while getting game"
        }), 400
    
    if not word_definitions_game:
        return jsonify({
            'error': "game not found"
        }), 400
    
    game_content, game_type, material_id = word_definitions_game

    if game_type != "word_definition_pairs":
        return jsonify({
            'error': "game_id is not word_definitions type"
        }), 400
    
    try:
        word_definitions = json.loads(game_content)
    except:
        return jsonify({
            'error': "error while parsing game content"
        }), 400

    try:
        grid, hints = generate_crossword(word_definitions, grid_size)
    except:
        return jsonify({
            'error': "error while generating crossword"
        }), 400
    
    crossword = {
        'grid': grid,
        'hints': hints
    }
    
    courceID = "0"
    gameType = "crossword"
    gameContent = json.dumps(crossword)
    materialID = material_id
    try:
        game_id = mongo.createGame(courceID, gameType, gameContent, materialID)
    except:
        return jsonify({
            'error': "error saving game"
        }), 400
    
    return jsonify({
        'crossword': crossword,
        'game_id': str(game_id)
    })


@game_bp.route('/wordsearch', methods=['POST'])
@require_token
def get_wordsearch():
    """
    Generate a wordsearch puzzle
    ---
    tags:
        - game
    consumes:
        - application/json
    parameters:
        - in: body
          name: body
          schema:
            required:
                - game_id
                - grid_size
            properties:
                game_id:
                    type: string
                grid_size:
                    type: integer
            example:
                game_id: 6552ba84a316097da00c9aa5
                grid_size: 20
    security:
        - ApiKeyAuth: []
    responses:
        200:
            description: A wordsearch puzzle
            schema:
                properties:
                    wordsearch:
                        type: object
                        grid:
                            type: array
                            items:
                                type: array
                                items:
                                    type: string
                        hints:
                            type: array
                            items:
                                type: string
                    game_id:
                        type: string
                example:
                    wordsearch: {
                        grid: [
                            ['V', 'Z', 'L', 'I', 'S', 'E', 'O', 'Y', 'K', 'W', 'U', 'G', 'G', 'U', 'D', 'H', 'T', 'K', 'Y', 'E'],
                            ['D', 'G', 'E', 'N', 'V', 'Z', 'D', 'A', 'T', 'E', 'L', 'I', 'G', 'A', 'J', 'G', 'C', 'B', 'V', 'E'],
                            ['E', 'L', 'M', 'T', 'L', 'A', 'Q', 'N', 'N', 'I', 'A', 'G', 'N', 'I', 'D', 'O', 'C', 'D', 'E', 'W'],
                            ['P', 'H', 'R', 'E', 'O', 'U', 'A', 'F', 'O', 'D', 'R', 'S', 'U', 'N', 'Q', 'S', 'J', 'M', 'T', 'P'],
                            ['L', 'E', 'U', 'G', 'C', 'O', 'X', 'T', 'V', 'I', 'E', 'U', 'I', 'K', 'E', 'O', 'Y', 'F', 'T', 'D'],
                            ['O', 'U', 'Z', 'R', 'K', 'S', 'I', 'E', 'D', 'A', 'T', 'R', 'C', 'I', 'F', 'S', 'T', 'W', 'O', 'U'],
                            ['Y', 'L', 'C', 'A', 'D', 'R', 'O', 'C', 'T', 'N', 'E', 'A', 'G', 'E', 'O', 'P', 'X', 'S', 'Q', 'Y'],
                            ['M', 'V', 'R', 'T', 'N', 'F', 'R', 'E', 'N', 'Q', 'K', 'O', 'Z', 'F', 'S', 'I', 'Z', 'K', 'B', 'B'],
                            ['E', 'U', 'U', 'I', 'H', 'Y', 'S', 'D', 'U', 'I', 'L', 'S', 'T', 'I', 'I', 'R', 'I', 'T', 'P', 'X'],
                            ['N', 'B', 'V', 'O', 'R', 'T', 'K', 'I', 'T', 'O', 'D', 'W', 'V', 'I', 'M', 'L', 'E', 'S', 'J', 'N'],
                            ['T', 'Q', 'O', 'N', 'I', 'Y', 'R', 'G', 'D', 'E', 'A', 'C', 'Y', 'A', 'E', 'I', 'R', 'B', 'O', 'Y'],
                            ['I', 'M', 'E', 'N', 'A', 'E', 'K', 'O', 'Q', 'R', 'D', 'Z', 'F', 'T', 'Q', 'W', 'T', 'Z', 'Y', 'X'],
                            ['O', 'Y', 'G', 'J', 'M', 'P', 'H', 'E', 'E', 'L', 'T', 'V', 'F', 'U', 'O', 'D', 'P', 'P', 'L', 'C'],
                            ['Y', 'J', 'F', 'E', 'P', 'T', 'K', 'O', 'A', 'I', 'P', 'O', 'X', 'Y', 'D', 'C', 'N', 'F', 'O', 'M'],
                            ['S', 'J', 'N', 'J', 'E', 'F', 'U', 'T', 'F', 'S', 'P', 'O', 'G', 'O', 'C', 'V', 'H', 'G', 'U', 'K'],
                            ['N', 'T', 'K', 'M', 'P', 'T', 'N', 'N', 'V', 'B', 'B', 'U', 'C', 'D', 'U', 'Q', 'B', 'W', 'O', 'G'],
                            ['S', 'B', 'P', 'A', 'E', 'A', 'H', 'C', 'R', 'B', 'A', 'A', 'P', 'G', 'F', 'H', 'O', 'U', 'O', 'T'],
                            ['B', 'T', 'N', 'E', 'M', 'P', 'O', 'L', 'E', 'V', 'E', 'D', 'B', 'Q', 'V', 'R', 'A', 'I', 'G', 'K'],
                            ['A', 'H', 'F', 'Q', 'Q', 'U', 'E', 'P', 'X', 'Z', 'P', 'Y', 'F', 'P', 'R', 'J', 'Q', 'C', 'L', 'I'],
                            ['D', 'B', 'J', 'F', 'V', 'K', 'M', 'A', 'I', 'N', 'T', 'E', 'N', 'A', 'N', 'C', 'E', 'E', 'H', 'T']
                        ],
                        hints: [
                            "A system of practices, techniques, procedures, and rules.",
                            "The protection of computer systems from theft or damage.",
                            "A description of what a software should do.",
                            "The process of making software better.",
                            "The process of writing and maintaining the source code.",
                            "The process of modifying software after delivery.",
                            "The process of combining software components.",
                            "The process of making software available for use.",
                            "A set of instructions that tells a computer what to do.",
                            "The process of evaluating software to find bugs.",
                            "The process of writing instructions for a computer.",
                            "A set of principles for software development."
                        ]
                    }
                    game_id: 6552b7cacdbae5d00cfcc7c4
        400:
            description: Bad request
            schema:
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

    if 'grid_size' not in data:
        return jsonify({
            'error': 'grid_size not provided'
        }), 400
    grid_size = data['grid_size']

    try:
        word_definitions_game = mongo.getGame(game_id)
    except:
        return jsonify({
            'error': "error while getting game"
        }), 400
    
    if not word_definitions_game:
        return jsonify({
            'error': "game not found"
        }), 400
    
    game_content, game_type, material_id = word_definitions_game

    if game_type != "word_definition_pairs":
        return jsonify({
            'error': "game_id is not word_definitions type"
        }), 400
    
    try:
        word_definitions = json.loads(game_content)
    except:
        return jsonify({
            'error': "error while parsing game content"
        }), 400

    try:
        grid, hints = generate_wordsearch(word_definitions, grid_size)
    except:
        return jsonify({
            'error': "error while generating wordsearch"
        }), 400
    
    wordsearch = {
        'grid': grid,
        'hints': hints
    }
    
    courceID = "0"
    gameType = "wordsearch"
    gameContent = json.dumps(wordsearch)
    materialID = material_id
    try:
        game_id = mongo.createGame(courceID, gameType, gameContent, materialID)
    except:
        return jsonify({
            'error': "error saving game"
        }), 400
    
    return jsonify({
        'wordsearch': wordsearch,
        'game_id': str(game_id)
    })