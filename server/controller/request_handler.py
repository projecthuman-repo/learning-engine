import threading

import uvicorn
from flask import Flask, request
from fastapi import FastAPI
from markupsafe import escape
from server.models.Crossword import crossword_parser
from server.models.Crossword import crossword_2 as crossword_methods
from pprint import pprint
import nltk
import server.controller.user_manager as user_manager
from server.models.Questgen import main
import server.models.UserData.user_data_classes as udc
import server.models.PDFExtract.pdf_extractor as pdfex


app = FastAPI()
um = user_manager.UserManager()
extractor = pdfex.Extractor()
RESPONSE = ""


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


#
@app.post("/user/")  # http://127.0.0.1:8000/user/?user_id=0
async def create_user(user_id: str):
    print("creating user")
    um.user_dict[user_id] = udc.User(user_id)
    print("user" + str(user_id) + "created")
    print("reading_pdf")
    txt = read_pdf("D:\pycharm_projecs\learning-engine\Academic_papers\\1-s2.0-S0092867421000118-main.pdf")
    print("pdf_read")
    print("\n")
    print(txt)
    print("\n")
    print("creating_tf_q")
    create_tf_question(user_id, txt)
    print("tfq_created")

    return "user" + str(user_id) + "created" + "txt"
def read_pdf(path:str):
    extractor.ocr_read(path)
    txt = extractor.get_text()
    txt = txt[0:250]
    payload = {"input_text": txt}
    return payload
def create_tf_question(user_id, payload):
    um.user_dict[user_id].courses['course_1'].modules['module_1'] \
        .concepts['concept_1'].games['tf'] = udc.TrueOrFalseGame(payload=payload)


@app.get("/user/")  # http://127.0.0.1:8000/user/?user_id=0&create=False
async def get_user(user_id: str):
    return um.user_dict[user_id]


# uvicorn server.controller.request_handler:app --reload
if __name__ == '__main__':
    print('[main]: starting...')
    uvicorn.run("server.controller.request_handler:app", host="127.0.0.1", port=8000, reload=True)