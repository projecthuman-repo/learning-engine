# Flask blueprint for document routes
from flask import Blueprint, request, jsonify
from ..models.document import extract_text_from_document
from ..database import mongo
from .auth.wrapper import require_token

document_bp = Blueprint('document', __name__)

@document_bp.route('/extract-text', methods=['POST'])
@require_token
def extract_text():
    """
    Extract text from a document (PDF and DOCX supported)
    ---
    tags:
        - document
    consumes:
        - multipart/form-data
    parameters:
        - in: formData
          name: document
          type: file
          required: true
          description: The document to extract text from
    security:
        - ApiKeyAuth: []
    responses:
        200:
            description: Text extracted from document
            schema:
                type: object
                properties:
                    text:
                        type: string
                        material_id: string
                example:
                    text: Software development is a dynamic and iterative process that transforms conceptual ideas into functional applications. It encompasses a diverse range of activities, including coding, testing, and maintenance, with an overarching goal of creating efficient, user-friendly software solutions. Development teams collaborate to design, build, and refine software, adhering to best practices and adapting to changing requirements. Agile methodologies promote flexibility and responsiveness, ensuring that software aligns with evolving user needs. Effective version control, debugging, and documentation are critical, fostering robust and reliable software. Continuous integration and deployment streamline the development pipeline, while cybersecurity and performance optimization safeguard against potential vulnerabilities. Software development is a dynamic, multifaceted field that powers modern digital innovation.
                    material_id: 6552b7cacdbae5d00cfcc7c4
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
    if 'document' not in request.files:
        return jsonify({
            'error': 'document not provided'
        }), 400
    document = request.files['document']
    
    try:
        text = extract_text_from_document(document.read())
    except:
        return jsonify({
            'error': 'error while extracting text from document'
        }), 400
    
    if text is None:
        return jsonify({
            'error': 'document type not supported'
        }), 400
    
    courseId = "0"
    courseMaterial = text
    courseDifficulty = None
    materialType = "text"
    accessType = "public"
    highlightedText = None
    
    try:
        material_id = mongo.createMaterial(courseId, courseMaterial, courseDifficulty, materialType, accessType, highlightedText)
    except:
        return jsonify({
            'error': 'error saving text to database'
        }), 400
    
    return jsonify({
        'text': text,
        'material_id': str(material_id)
    })