# Flask Blueprint for LLM routes.
import json
from flask import Blueprint, request, jsonify
from ..models.llm import getModel
from ..database import mongo
from .auth.wrapper import require_token

llm_bp = Blueprint('llm', __name__)
llm_model = getModel()

@llm_bp.route('/generate-word-definition-pairs', methods=['POST'])
@require_token
def generate_word_definition_pairs():
    """
    Generate word definition pairs from text
    ---
    tags:
        - llm
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
                count:
                    type: integer
            example:
                material_id: 6552b7cacdbae5d00cfcc7c4
                count: 5
    security:
        - ApiKeyAuth: []
    responses:
        200:
            description: Word definition pairs
            schema:
                properties:
                    word_definitions:
                        type: array
                        items:
                            type: object
                            properties:
                                Word:
                                    type: string
                                Definition:
                                    type: string
                    game_id:
                        type: string
                example:
                    word_definitions: [
                        {
                            "Word": "Software", 
                            "Definition": "A set of instructions that tells a computer what to do."
                        },
                        {
                            "Word": "Development",
                            "Definition": "The process of writing and maintaining the source code."
                        },
                        {
                            "Word": "Agile",
                            "Definition": "A set of principles for software development."
                        },
                        {
                            "Word": "Methodologies",
                            "Definition": "A system of practices, techniques, procedures, and rules."
                        },
                        {
                            "Word": "Coding",
                            "Definition": "The process of writing instructions for a computer."
                        },
                        {
                            "Word": "Testing",
                            "Definition": "The process of evaluating software to find bugs."
                        },
                        {
                            "Word": "Maintenance",
                            "Definition": "The process of modifying software after delivery."
                        },
                        {
                            "Word": "Requirements",
                            "Definition": "A description of what a software should do."
                        },
                        {
                            "Word": "Integration",
                            "Definition": "The process of combining software components."
                        },
                        {
                            "Word": "Deployment",
                            "Definition": "The process of making software available for use."
                        },
                        {
                            "Word": "Cybersecurity",
                            "Definition": "The protection of computer systems from theft or damage."
                        },
                        {
                            "Word": "Optimization",
                            "Definition": "The process of making software better."
                        }
                    ]
                    game_id: 6552b7cacdbae5d00cfcc7c4
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
    count = data['count'] if 'count' in data else 10

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

    try:
        word_definition_pairs = llm_model.wordDefinition(count, text)
    except:
        return jsonify({
            'error': 'error generating word definition pairs'
        }), 400


    courceID = "0"
    gameType = "word_definition_pairs"
    gameContent = json.dumps(word_definition_pairs)
    materialID = material_id
    try:
        game_id = mongo.createGame(courceID, gameType, gameContent, materialID)
    except:
        return jsonify({
            'error': "error saving game"
        }), 400

    return jsonify({
        'word_definitions': word_definition_pairs,
        'game_id': str(game_id)
    })

@llm_bp.route('/generate-mcqs', methods=['POST'])
@require_token
def generate_mcqs():
    """
    Generate MCQs from text
    ---
    tags:
        - llm
    consumes:
        - application/json
    parameters:
        - in: body
          name: body
          schema:
            required:
                - text
            properties:
                material_id:
                    type: string
                count:
                    type: integer
            example:
                material_id: 6552b7cacdbae5d00cfcc7c4
                count: 10
    security:
        - ApiKeyAuth: []
    responses:
        200:
            description: Multiple choice questions
            schema:
                properties:
                    mcqs:
                        type: array
                        items:
                            type: object
                            required:
                                - question
                                - options
                                - answer
                            properties:
                                question:
                                    type: string
                                options:
                                    type: array
                                    items:
                                        type: string
                                answer:
                                    type: string
                    game_id:
                        type: string
                example:
                    mcqs: [
                        {
                            "question": "What is the capital of India?",
                            "options": [
                                "New Delhi",
                                "Mumbai",
                                "Kolkata",
                                "Chennai"
                            ],
                            "answer": 0
                        },
                        {
                            "question": "How many countries are there in the world?",
                            "options": [
                                "195",
                                "196",
                                "197",
                                "198"
                            ],
                            "answer": 1
                        },
                        {
                            "question": "Which is the largest country by land area?",
                            "options": [
                                "Russia",
                                "Canada",
                                "China",
                                "USA"
                            ],
                            "answer": 0
                        }
                    ] 
                    game_id: 6552b7cacdbae5d00cfcc7c4
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
    count = data['count'] if 'count' in data else 10

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

    try:
        mcqs = llm_model.mcq(count, text)
    except:
        return jsonify({
            'error': 'error generating mcqs'
        }), 400
    
    courceID = "0"
    gameType = "mcqs"
    gameContent = json.dumps(mcqs)
    materialID = material_id
    try:
        game_id = mongo.createGame(courceID, gameType, gameContent, materialID)
    except:
        return jsonify({
            'error': "error saving game"
        }), 400
    
    return jsonify({
        'mcqs': mcqs,
        'game_id': str(game_id)
    })

@llm_bp.route('/generate-fill-in-the-blanks', methods=['POST'])
@require_token
def generate_fill_in_the_blanks():
    """
    Generate fill-in-the-blanks questions from text 
    ---
    tags:
        - llm
    consumes:
        - application/json
    parameters:
        - in: body
          name: body
          schema:
            required:
                - text
            properties:
                material_id:
                    type: string
                count:
                    type: integer
            example:
                material_id: 6552b7cacdbae5d00cfcc7c4
                count: 2
    security:
        - ApiKeyAuth: []
    responses:
        200:
            description: Fill-in-the-blanks questions
            schema:
                properties:
                    fill_in_the_blanks:
                        type: array
                        items:
                            type: object
                            required:
                                - question
                                - answer
                            properties:
                                Question:
                                    type: string
                                Answer:
                                    type: string
                    game_id:
                        type: string
                example:
                    fill_in_the_blanks: [
                        {
                            "Question": "It is a sunny ____.",
                            "Answer": "day"
                        },
                        {
                            "Question": "A ____________ is a computer program that can harm your computer.",
                            "Answer": "virus"
                        }
                    ]
                    game_id: 6552b7cacdbae5d00cfcc7c4
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
    count = data['count'] if 'count' in data else 10

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

    try:
        fill_in_the_blanks = llm_model.fillInTheBlanks(count, text)
    except:
        return jsonify({
            'error': 'error while generating fill-in-the-blanks questions'
        }), 400
    
    courceID = "0"
    gameType = "fill_in_the_blanks"
    gameContent = json.dumps(fill_in_the_blanks)
    materialID = material_id
    try:
        game_id = mongo.createGame(courceID, gameType, gameContent, materialID)
    except:
        return jsonify({
            'error': "error saving game"
        }), 400
    
    return jsonify({
        'fill_in_the_blanks': fill_in_the_blanks,
        'game_id': str(game_id)
    })

@llm_bp.route('/generate-short-answers', methods=['POST'])
@require_token
def generate_short_answers():
    """
    Generate short answer questions from text 
    ---
    tags:
        - llm
    consumes:
        - application/json
    parameters:
        - in: body
          name: body
          schema:
            required:
                - text
            properties:
                material_id:
                    type: string
                count:
                    type: integer
            example:
                material_id: 6552b7cacdbae5d00cfcc7c4
                count: 2
    security:
        - ApiKeyAuth: []
    responses:
        200:
            description: Short answer questions
            schema:
                properties:
                    short_answers:
                        type: array
                        items:
                            type: object
                            required:
                                - Question
                                - Answer
                            properties:
                                Question:
                                    type: string
                                Answer:
                                    type: string
                    game_id:
                        type: string
                example:
                    short_answers: [
                        {
                            "Question": "What is sunny?",
                            "Answer": "Weather"
                        },
                        {
                            "Question": "What can harm your computer?",
                            "Answer": "Virus"
                        }
                    ]
                    game_id: 6552b7cacdbae5d00cfcc7c4
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
    count = data['count'] if 'count' in data else 10

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

    try:
        short_answers = llm_model.shortAnswer(count, text)
    except:
        return jsonify({
            'error': 'error while generating short answer questions'
        }), 400
    
    courceID = "0"
    gameType = "short_answers"
    gameContent = json.dumps(short_answers)
    materialID = material_id
    try:
        game_id = mongo.createGame(courceID, gameType, gameContent, materialID)
    except:
        return jsonify({
            'error': "error saving game"
        }), 400
    
    return jsonify({
        'short_answers': short_answers,
        'game_id': str(game_id)
    })
