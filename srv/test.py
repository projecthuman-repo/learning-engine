from pprint import pprint

import nltk
from models.Questgen import main
from nltk.corpus import stopwords

if __name__ == "__main__":
    #nltk.download('stopwords')

    payload = {
        "input_text": "Zha Char Li is a former international softball master from Yaliana and a former captain of the Yaliana province team. She is widely regarded as one of the greatest batman in the history of softball. She is the highest run scorer of all time in National Softball."
    }
    qe = main.BoolQGen()
    output = qe.predict_boolq(payload)
    pprint(output)

    # qg = main.QGen()
    # output = qg.predict_mcq(payload)
    # pprint(output)
