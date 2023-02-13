from flask import Flask,request
app = Flask(__name__)
@app.route('/get/<path:sub_path>', methods=['GET'])
def handle_get(sub_path):
    return get_options[sub_path]

@app.route('/get/<path:sub_path>', methods=['POST'])
def handle_post(sub_path):
    return post_options[sub_path]
from markupsafe import escape
from server.models.Crossword import crossword_parser
from server.models.Crossword import crossword_2 as crossword_methods
# flask --app hello run



def hello_world():
    return 'Hello, World'

def print_crossword_grid():
    a = crossword_methods.run(print_cross=False)
    return a
    #return "1"

get_options = {
    'hello': hello_world(),
    'print_crossword_grid': print_crossword_grid()
}

post_options = {
    'hello': hello_world()
}




# flask --app RequestHandler run
# flask RequestHandler run
