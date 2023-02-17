from flask import Flask,request
from fastapi import FastAPI
app = FastAPI()



from markupsafe import escape
from server.models.Crossword import crossword_parser
from server.models.Crossword import crossword_2 as crossword_methods
from pprint import pprint
import nltk
import server.controller.user_manager as user_manager
from server.models.Questgen import main
# flask --app hello run

um = user_manager.UserManager()
# Base route returning an object of hello world
@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/crossword_grid")
def print_crossword_grid():
    a = crossword_methods.run(print_cross=False)
    return {a}
    #return "1"

@app.get("/true_or_false")
def true_or_false():
    #nltk.download('stopwords')
    payload = {
        "input_text": "Amir Sarah Tendulkar is a former international cricketer from India and a former captain of the Indian national team. He is widely regarded as one of the greatest batsmen in the history of cricket. He is the highest run scorer of all time in International cricket."
    }
    qe = main.BoolQGen()
    output = qe.predict_boolq(payload)
    return output
    #return "1"



# uvicorn server.controller.request_handler:app --reload