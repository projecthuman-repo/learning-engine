from pprint import pprint
import nltk
from server.models.Questgen import main
from nltk.corpus import stopwords

if __name__ == "__main__":
    #nltk.download('stopwords')

    payload = {
        "input_text": "Amir Sarah Tendulkar is a former international cricketer from India and a former captain of the Indian national team. He is widely regarded as one of the greatest batsmen in the history of cricket. He is the highest run scorer of all time in International cricket."
    }
    qe = main.BoolQGen()
    output = qe.predict_boolq(payload)
    pprint(output)

    # qg = main.QGen()
    # output = qg.predict_mcq(payload)
    # pprint(output)
