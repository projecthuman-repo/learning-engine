from flask import Flask,request
app = Flask(__name__)



from markupsafe import escape
from server.models.Crossword import crossword_parser
from server.models.Crossword import crossword_2 as crossword_methods
from pprint import pprint
import nltk
from server.models.Questgen import main
# flask --app hello run


@app.route('/get/hello', methods=['GET'])
def hello_world():
    return 'Hello, World'


@app.route('/get/crossword_grid', methods=['GET'])
def print_crossword_grid():
    a = crossword_methods.run(print_cross=False)
    return a
    #return "1"

@app.route('/get/true_or_false', methods=['GET'])
def true_or_false():
    #nltk.download('stopwords')
    payload = {
        "input_text": "Amir Sarah Tendulkar is a former international cricketer from India and a former captain of the Indian national team. He is widely regarded as one of the greatest batsmen in the history of cricket. He is the highest run scorer of all time in International cricket."
    }
    qe = main.BoolQGen()
    output = qe.predict_boolq(payload)
    return output
    #return "1"

# GET requests will be blocked
@app.route('/json-example', methods=['POST'])
def json_example():
    request_data = request.get_json()

    language = request_data['language']
    framework = request_data['framework']

    # two keys are needed because of the nested object
    python_version = request_data['version_info']['python']

    # an index is needed because of the array
    example = request_data['examples'][0]

    boolean_test = request_data['boolean_test']

    return '''
           The language value is: {}
           The framework value is: {}
           The Python version is: {}
           The item at index 0 in the example list is: {}
           The boolean value is: {}'''.format(language, framework, python_version, example, boolean_test)

# flask --app RequestHandler run
# flask RequestHandler run
if __name__ == '__main__':
    app.run(host= '0.0.0.0',debug=True)