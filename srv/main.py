import sys
import os
myDir = os.getcwd()
sys.path.append(myDir)
from pathlib import Path
path = Path(myDir)
a=str(path.parent.absolute())

sys.path.append(a)

import threading

# import json
# import uvicorn
from flask import Flask, request, jsonify,Blueprint,render_template,redirect
# from flask_restx import Resource, Api, fields
#from flask_restx.api import swagger
from flasgger import Swagger,swag_from
# from fastapi import FastAPI
import jsonpickle
# from markupsafe import escape
# from srv.models.Crossword import crossword_parser
from srv.models.Crossword import crossword_2 as crossword_methods
# from pprint import pprint
from srv.controller.user_manager import UserManager
from srv.models.Questgen import main
from srv.models.LeafAI.mcq_generation import MCQGenerator
from srv.models.WordSearch.WordSearch import WordSearch
import srv.models.UserData.user_data_classes as udc
from srv.models.PDFExtract.pdf_extractor import Extractor
from srv.server_constants import *



app = Flask(__name__)
Swagger(app)
um = UserManager()
extractor = Extractor()
tf_gen = main.BoolQGen()
mc_gen = MCQGenerator(False)
RESPONSE = ""


def init_BoolQGen(self, payload):
    qe = main.BoolQGen()
    self.data = qe.predict_boolq(payload)
    self.data["answer"] = 2  # 0 = False 1 = True, 2/other num = uninitialized
# Base route returning an object of hello world
@app.route('/')
def hello_world() -> str:
    return "Hello, World!"


@app.route('/crossword_grid', methods=['GET'])
def print_crossword_grid():
    if request.method == 'POST':
        a = crossword_methods.run(print_cross=False)
        return {a}

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

@app.route('/items/', methods=['POST'])
def read_item():  # http://127.0.0.1:8000/items/?skip=0&limit=10
    error = None
    if request.method == 'POST':
        skip = request.form['skip']
        limit = request.form['limit']
        return fake_items_db[skip: skip + limit]
    else:
        error = 'Invalid parameters'
        return error


 # http://127.0.0.1:8000/user/?user_id=0
@app.route('/user/', methods=['GET', 'POST'])
def initiate_user():
    #user_id = request.form['user_id']
    user_id = request.args.get('user_id', None)
    if request.method == 'POST':
        create_user(user_id)
        um.create_course(user_id,course_title="course_1")
        um.create_module(user_id,course_title="course_1",module_title="module_1")
        um.create_concept(user_id,
                          course_title="course_1",
                          module_title="module_1",
                          concept_title="concept_1")
        return "user" + str(user_id) + "created" + "txt"
    elif request.method == 'GET':
        if user_id == "dummy":  # some inappropriate usage just for simpler testing
            create_dummy_user()
        return jsonpickle.encode(um.user_dict[user_id],unpicklable=False,indent=4)
        # unpickable avoids producing "py/obj" values; indent allows pretty printed view

    # print("reading_pdf")
    # txt = read_pdf(pdf_extractor_constants.TEMP_PDF_PATH)
    # print("pdf_read")
    # print("\n")
    # print(txt)
    # print("\n")
    # print("creating_tf_q")
    # create_tf_game(txt, user_id,
    #                   course_title="course_1",
    #                   module_title="module_1",
    #                   concept_title="concept_1")
    # print("tfq_created")





def create_tf_game(txt, user_id,
                  course_title="course_1",
                  module_title="module_1",
                  concept_title="concept_1"):
    data = tf_gen.predict_boolq(txt)

    for bool_q_count in range(len(data["Boolean Questions"])):
        reformated_data = {"text": data["Text"],
                           "question": data["Boolean Questions"][bool_q_count],
                           "answer": None}
        um.create_game(user_id,
                          course_title=course_title,
                          module_title=module_title,
                          concept_title=concept_title,
                          data=reformated_data,game_type="TF")

def create_mc_game(txt, user_id,
                  course_title="course_1",
                  module_title="module_1",
                  concept_title="concept_1"):
    # multiple choice (LeafAI)
    question = mc_gen.generate_mcq_questions(txt, 8)
    for index in range(len(question)):
        um.create_game(user_id,
                       course_title=course_title,
                       module_title=module_title,
                       concept_title=concept_title,
                       data=question[index], game_type="MC")



def create_cw_game(user_id, course_title, module_title, concept_title):
    data = crossword_methods.run(print_cross=True,
                          crossword_txt_path=CROSSWORD_TXT_PATH)
    um.create_game(user_id,
                      course_title=course_title,
                      module_title=module_title,
                      concept_title=concept_title,
                      data=data, game_type="CW")


 # http://127.0.0.1:8000/user/initiate_cw_game/?user_id=0&cw=1
@app.route('/user/initiate_cw_game', methods=['POST'])
def initiate_cw_game():
    #user_id = request.form['user_id']
    user_id = request.args.get('user_id', None)
    if request.method == 'POST':
        print("creating_cw_game")
        create_cw_game(user_id,
                      course_title="course_1",
                      module_title="module_1",
                      concept_title="concept_1"),

def create_ws_game(txt, user_id,
                   course_title="course_1",
                   module_title="module_1",
                   concept_title="concept_1"):
    # word search game (WordSearch)

    words = txt

    words_lst = words.split(',')
    grid_len = len(max(words_lst, key=len)) + 2
    w = WordSearch(words, grid_len, grid_len)
    w.findWords(words.split(','))
    data = {"grid": w.grid, "positions": w.wordPosition}
    um.create_game(user_id,
                      course_title=course_title,
                      module_title=module_title,
                      concept_title=concept_title,
                      data=data, game_type="WS")
def create_fitb_game(txt, user_id,
                   course_title="course_1",
                   module_title="module_1",
                   concept_title="concept_1"):
    # fill in the blank (LeafAI)
    context = txt
    # Obtain the answers from the generation of the multiple choice questions.
    questions = mc_gen.generate_mcq_questions(context, 8)
    # Obtain the sentence in which these answers appear in order to create the fill-in-the-blank.
    context_splits = mc_gen._split_context_according_to_desired_count(context, 8)
    # Find the index at which the answer starts in the sentence in order to help with the fill in the blank generation (i.e removing the answer)
    # from the sentence.
    start_idx = []
    i = 0
    # This algorithm cannot find the start of the answer "60-85 cm" for the sentence "The koala has a body length of 60–85 cm (24–33 in) and weighs 4–15 kg (9–33 lb)."
    # However, it should not be an issue if the pre-processing of the texts replace the special character "–" with "-". This could be a re-occuring issue.
    for sentence, answer in zip(context_splits, questions):

        start_idx.append(sentence.lower().find(answer.answerText.lower()))

        data = {"sentence": sentence, "keyword": answer.answerText, "start_index": start_idx[i]}
        um.create_game(user_id,
                       course_title=course_title,
                       module_title=module_title,
                       concept_title=concept_title,
                       data=data, game_type="FITB")
        i = i + 1


def create_dm_game(txt, user_id,
                   course_title="course_1",
                   module_title="module_1",
                   concept_title="concept_1"):
    # 1. generate game data
    data = {"word":"def", "a":"the first letter in alphabet", "b":"the second letter in alphabet"}
    # definition match
    um.create_game(user_id,
                   course_title="course_1",
                   module_title="module_1",
                   concept_title="concept_1",
                   data = data,
                   game_type = "DM"),

def create_user(user_id):
    print("creating user")
    um.user_dict[user_id] = udc.User(user_id)
    print("user" + str(user_id) + "created")
def read_pdf(path:str):
    extractor.ocr_read(path)
    txt = extractor.get_text()
    txt = txt[0:250]
    payload = {"input_text": txt}
    return payload
 # http://127.0.0.1:8000/user/?user_id=0
@app.route('/pdf/', methods=['POST'])
def convert_pdf():
    #user_id = request.form['user_id']
    user_id = request.args.get('user_id', None)
    payload = None
    if request.method == 'POST':
        extractor.ocr_read(request.files['pdf_file_name'])
        txt = extractor.get_text()
        txt = txt[0:250]
        payload = {"input_text": txt}
    return payload






def create_dummy_user():
    user_id = "dummy"
    course_title = "course_1"
    module_title = "module_1"
    concept_title = "concept_1"

    leaf_context = '''The koala or, inaccurately, koala bear[a] (Phascolarctos cinereus), is an arboreal herbivorous marsupial native to Australia. It is the only extant representative of the family Phascolarctidae and its closest living relatives are the wombats, which are members of the family Vombatidae. The koala is found in coastal areas of the mainland's eastern and southern regions, inhabiting Queensland, New South Wales, Victoria, and South Australia. It is easily recognisable by its stout, tailless body and large head with round, fluffy ears and large, spoon-shaped nose. The koala has a body length of 60–85 cm (24–33 in) and weighs 4–15 kg (9–33 lb). Fur colour ranges from silver grey to chocolate brown. Koalas from the northern populations are typically smaller and lighter in colour than their counterparts further south. These populations possibly are separate subspecies, but this is disputed.'''
    payload = {
        "input_text": "Amir Sarah Tendulkar is a former international cricketer from India and a former captain of the Indian national team. He is widely regarded as one of the greatest batsmen in the history of cricket. He is the highest run scorer of all time in International cricket."
    }

    create_user(user_id)
    um.create_course(user_id, course_title=course_title)
    um.create_module(user_id, course_title=course_title, module_title=module_title)
    um.create_concept(user_id,
                      course_title=course_title,
                      module_title=module_title,
                      concept_title=concept_title)
    create_tf_game(txt=payload, user_id=user_id,
                      course_title=course_title,
                      module_title=module_title,
                      concept_title=concept_title)
    create_mc_game(txt=leaf_context, user_id=user_id,
                      course_title=course_title,
                      module_title=module_title,
                      concept_title=concept_title)
    create_cw_game(user_id=user_id,
                      course_title=course_title,
                      module_title=module_title,
                      concept_title=concept_title)
    create_ws_game(txt=("Gugu,Gaga"), user_id=user_id,
                   course_title=course_title,
                   module_title=module_title,
                   concept_title=concept_title)
    create_fitb_game(txt=leaf_context, user_id=user_id,
                   course_title=course_title,
                   module_title=module_title,
                   concept_title=concept_title)
    create_dm_game(txt="unused",user_id=user_id,
                   course_title=course_title,
                   module_title=module_title,
                   concept_title=concept_title)
# uvicorn srv.controller.request_handler:app --reload

# flask --app YOUR_PREV_PATH'S\srv\controller\main.py run
if __name__ == '__main__':
    print('[main]: starting...')

    app.run(host='127.0.0.1', port=8080, debug=False)
    # uvicorn.run("srv.controller.request_handler:app", host="127.0.0.1", port=8000, reload=False)
    # reload=True means if you edit main.py while the srv is running, it will auto-rerun the srv
    #create_dummy_user()



