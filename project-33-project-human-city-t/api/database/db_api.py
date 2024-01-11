from flask import Flask, jsonify, request, make_response
from flask_restful import Resource, Api
import re
from flask_swagger_ui import get_swaggerui_blueprint
import json
import sys
sys.path.append('../db/')
import mongo

app = Flask(__name__)
api = Api(app)


#Function to "highlight" content to emphasize what instructors would like LLM to do 
def colorCode(content: str, highlights: list[str]):
    updatedStr = content
    underline = "*"
    for i in highlights:
        updatedStr = updatedStr.replace(i, underline + i + underline)
        underline += "*"
    return updatedStr


class GetMaterial(Resource):
    def get(self):
        parameterValue = request.args.get("courseId")
        if parameterValue:
            if mongo.getCourse(parameterValue) is None:
                return  make_response(jsonify(error="Not Found: Value not found"), 404)

            retVal = mongo.getMaterial(parameterValue)
            if retVal:
                colorCode_str = ""
                for i in retVal:
                    colorCode_str += colorCode(i[0], i[2])
                return jsonify({'Content': colorCode_str})
            else:
                return make_response(jsonify(error="Not Found: Value not found"), 404)
        else:
            return make_response(jsonify(error="Bad Request: Invalid value"), 400)

api.add_resource(GetMaterial, '/material/get')

class createMaterial(Resource):
    def post(self):

        try:
            inputs = request.get_json()

            # Access the input parameters
            courseId = inputs['courseId']
            courseMaterial = inputs['courseMaterial']
            courseDifficulty = inputs['courseDifficulty']
            materialType = inputs['materialType']
            accessType = inputs['accessType']

            if not (courseId and courseMaterial and courseDifficulty and materialType and accessType ):
                return  make_response(jsonify(error="Bad Request: Invalid value"), 400)
            
            if mongo.getCourse(courseId) is None:
                return  make_response(jsonify(error="Not Found: Value not found"), 404)


            # TBD: Depending on how the other subteam reads content from pdf, read highlighted words and 
            # store them appropriately so they can be sent to LLM
            if mongo.createMaterial(courseId, courseMaterial, courseDifficulty, materialType, accessType, []) == 0:
                return make_response(jsonify(error="Data posted successfully"), 200)
            else: 
                return make_response(jsonify(error="Not Found: Value not found"), 404)
            
        except Exception as e:
            return make_response(jsonify(error="Bad Request: Invalid value"), 400)

api.add_resource(createMaterial, '/material/create')


class GetGame(Resource):
    def get(self):
        courseId = request.args.get("courseId")
        gameType = request.args.get("gameType")
        materialId = request.args.get("materialId")

        if courseId and gameType and materialId:

            if not mongo.getCourse(courseId):
                return  make_response(jsonify(error="Bad Request: Invalid value"), 400)

            retVal = mongo.getGame(courseId, gameType, materialId )
            if retVal:
                return jsonify({'Game': retVal})
            else:
                return make_response(jsonify(error="Not Found: Value not found"), 404)
        else:
            return make_response(jsonify(error="Bad Request: Invalid value"), 400)

api.add_resource(GetGame, '/game/get')


class CreateGame(Resource):
    def get(self):
        courseId = request.args.get("courseId")
        gameType = request.args.get("gameType")
        materialId = request.args.get("materialId")
        gameContent = request.args.get("gameContent")

        if not mongo.getCourse(courseId):
            return  make_response(jsonify(error="Bad Request: Invalid value"), 400)

        if courseId and gameType and materialId and gameContent:
            retVal = mongo.getGame(courseId, gameType, gameContent, materialId)
            if retVal:
                return jsonify({'Content': retVal})
            else:
                return make_response(jsonify(error="Not Found: Value not found"), 404)
        else:
            return make_response(jsonify(error="Bad Request: Invalid value"), 400)

api.add_resource(CreateGame, '/game/create')


# Configure Swagger UI
SWAGGER_URL = '/swagger'
API_URL = 'http://127.0.0.1:5000/swagger.json'
swaggeruiBlueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Sample API"
    }
)
app.register_blueprint(swaggeruiBlueprint, url_prefix=SWAGGER_URL)

@app.route('/swagger.json')
def swagger():
    with open('swagger.json', 'r') as f:
        return jsonify(json.load(f))

if __name__ == '__main__':
    app.run(debug=True)


