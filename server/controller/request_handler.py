import threading

import uvicorn
from flask import Flask, request
from fastapi import FastAPI
from markupsafe import escape
from server.models.Crossword import crossword_parser
from server.models.Crossword import crossword_2 as crossword_methods
from pprint import pprint
from server.controller.user_manager import UserManager
from server.models.Questgen import main
import server.models.UserData.user_data_classes as udc
from server.models.PDFExtract.pdf_extractor import Extractor
from server.server_constants import *


app = FastAPI()
um = UserManager()
extractor = Extractor()
tf_gen = main.BoolQGen()
RESPONSE = ""


def init_BoolQGen(self, payload):
    qe = main.BoolQGen()
    self.data = qe.predict_boolq(payload)
    self.data["answer"] = 2  # 0 = False 1 = True, 2/other num = uninitialized
# Base route returning an object of hello world
@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/crossword_grid")
def print_crossword_grid():
    a = crossword_methods.run(print_cross=False)
    return {a}

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


@app.get("/items/")
async def read_item(skip: int = 0, limit: int = 10):  # http://127.0.0.1:8000/items/?skip=0&limit=10
    return fake_items_db[skip: skip + limit]

@app.post("/user/")  # http://127.0.0.1:8000/user/?user_id=0
async def initiate_user(user_id: str):

    create_user(user_id)
    um.create_course(user_id,course_title="course_1")
    um.create_module(user_id,course_title="course_1",module_title="module_1")
    um.create_concept(user_id,
                      course_title="course_1",
                      module_title="module_1",
                      concept_title="concept_1")

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

    return "user" + str(user_id) + "created" + "txt"




def create_tf_game(txt, user_id,
                  course_title="course_1",
                  module_title="module_1",
                  concept_title="concept_1"):
    data = tf_gen.predict_boolq(txt)

    for bool_q_count in range(len(data["Boolean Questions"])):
        reformated_data = {"text": data["Text"],
                           "question": data["Boolean Questions"][bool_q_count],
                           "answer": None}
        um.create_tf_game(user_id,
                          course_title=course_title,
                          module_title=module_title,
                          concept_title=concept_title,
                          data=reformated_data)

def create_mc_game(txt, user_id,
                  course_title="course_1",
                  module_title="module_1",
                  concept_title="concept_1"):
    # multiple choice (LeafAI)
    a = 1


def create_cw_game(user_id, course_title, module_title, concept_title):
    data = crossword_methods.run(print_cross=True,
                          crossword_txt_path=CROSSWORD_TXT_PATH)
    um.create_cw_game(user_id,
                      course_title=course_title,
                      module_title=module_title,
                      concept_title=concept_title,
                      data=data)


@app.post("/user/initiate_cw_game")  # http://127.0.0.1:8000/user/initiate_cw_game/?user_id=0&cw=1
async def initiate_cw_game(user_id: str, cw: str):
    if cw == "1":
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
    a = 1
def create_fitb_game(txt, user_id,
                   course_title="course_1",
                   module_title="module_1",
                   concept_title="concept_1"):
    # fill in the blank (LeafAI)
    a = 1

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
@app.post("/user/")  # http://127.0.0.1:8000/user/?user_id=0
async def convert_pdf(user_id: str, convert_pdf: bool = True):
    extractor.ocr_read(TEMP_PDF_PATH)
    txt = extractor.get_text()
    txt = txt[0:250]
    payload = {"input_text": txt}
    return payload

@app.get("/user/")  # http://127.0.0.1:8000/user/?user_id=0&create=False
async def get_user(user_id: str):
    if user_id == "dummy": # some inappropriate usage just for simpler testing
        create_dummy_user()
    return um.user_dict[user_id]



def create_dummy_user():
    user_id = "dummy"
    course_title = "course_1"
    module_title = "module_1"
    concept_title = "concept_1"

    leaf_context = '''The koala or, inaccurately, koala bear[a] (Phascolarctos cinereus), is an arboreal herbivorous marsupial native to Australia. It is the only extant representative of the family Phascolarctidae and its closest living relatives are the wombats, which are members of the family Vombatidae. The koala is found in coastal areas of the mainland's eastern and southern regions, inhabiting Queensland, New South Wales, Victoria, and South Australia. It is easily recognisable by its stout, tailless body and large head with round, fluffy ears and large, spoon-shaped nose. The koala has a body length of 60–85 cm (24–33 in) and weighs 4–15 kg (9–33 lb). Fur colour ranges from silver grey to chocolate brown. Koalas from the northern populations are typically smaller and lighter in colour than their counterparts further south. These populations possibly are separate subspecies, but this is disputed.'''


    create_user(user_id)
    um.create_course(user_id, course_title=course_title)
    um.create_module(user_id, course_title=course_title, module_title=module_title)
    um.create_concept(user_id,
                      course_title=course_title,
                      module_title=module_title,
                      concept_title=concept_title)
    create_cw_game(user_id=user_id,
                      course_title=course_title,
                      module_title=module_title,
                      concept_title=concept_title)
    create_dm_game(txt="unused",user_id=user_id,
                   course_title=course_title,
                   module_title=module_title,
                   concept_title=concept_title)
    create_fitb_game(txt="unused", user_id=user_id,
                   course_title=course_title,
                   module_title=module_title,
                   concept_title=concept_title)
# uvicorn server.controller.request_handler:app --reload
if __name__ == '__main__':
    print('[main]: starting...')

    uvicorn.run("server.controller.request_handler:app", host="127.0.0.1", port=8000, reload=False)
    # reload=True means if you edit request_handler.py while the server is running, it will auto-rerun the server
    create_dummy_user()