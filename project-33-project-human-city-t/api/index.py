from flask import Flask
from flasgger import Swagger

from blueprints.api import api


SWAGGER_TEMPLATE = {
    "securityDefinitions": {
        "ApiKeyAuth": {
            "type": "apiKey",
            "name": "token",
            "in": "header"
        }
    }
}

app = Flask(__name__)
swagger = Swagger(app, template=SWAGGER_TEMPLATE)

app.register_blueprint(api, url_prefix='/api')

@app.route('/')
def home():
    return "Hello world!"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)