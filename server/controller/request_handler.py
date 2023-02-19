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
import server.models.PDFExtract.pdf_extractor_constants as pdf_extractor_constants



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
    # return "1"


# @app.get("/true_or_false")
# def true_or_false():
#     #nltk.download('stopwords')
#     payload = {
#         "input_text": "Amir Sarah Tendulkar is a former international cricketer from India and a former captain of the Indian national team. He is widely regarded as one of the greatest batsmen in the history of cricket. He is the highest run scorer of all time in International cricket."
#     }
#     qe = main.BoolQGen()
#     output = qe.predict_boolq(payload)
#     return output
#     #return "1"

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

    print("reading_pdf")
    txt = read_pdf(pdf_extractor_constants.TEMP_PDF_PATH)
    print("pdf_read")
    print("\n")
    print(txt)
    print("\n")
    print("creating_tf_q")
    create_tf_game(txt, user_id,
                      course_title="course_1",
                      module_title="module_1",
                      concept_title="concept_1")
    print("tfq_created")

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
    extractor.ocr_read(pdf_extractor_constants.TEMP_PDF_PATH)
    txt = extractor.get_text()
    txt = txt[0:250]
    payload = {"input_text": txt}
    return payload

@app.get("/user/")  # http://127.0.0.1:8000/user/?user_id=0&create=False
async def get_user(user_id: str):
    return um.user_dict[user_id]


# uvicorn server.controller.request_handler:app --reload
if __name__ == '__main__':
    print('[main]: starting...')
    uvicorn.run("server.controller.request_handler:app", host="127.0.0.1", port=8000, reload=True)