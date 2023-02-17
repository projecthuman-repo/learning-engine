from abc import ABC, abstractmethod
from server.models.Questgen import main
import threading


class Game(ABC):
    def __init__(self):
        self.data = None

    def get_data(self):
        return self.data


class TrueOrFalseGame(Game):

    def __init__(self, payload):
        super().__init__()
        t = threading.Thread(target=self.init_BoolQGen(payload))
        t.start()

    def init_BoolQGen(self,payload):
        qe = main.BoolQGen()
        self.data = qe.predict_boolq(payload)
        self.data["answer"] = 2  # 0 = False 1 = True, 2/other num = uninitialized


class Concepts():
    def __init__(self):
        self.games = {}
        # self.games["tf"] = TrueOrFalseGame(payload={
        #     "input_text": "Amir Sarah Tendulkar is a former international cricketer from India and a former captain of the Indian national team. He is widely regarded as one of the greatest batsmen in the history of cricket. He is the highest run scorer of all time in International cricket."
        # })


class Module():
    def __init__(self):
        self.concepts = {}
        self.concepts["concept_1"] = Concepts()


class Course():
    def __init__(self):
        self.modules = {}
        self.modules["module_1"] = Module()


class User():
    def __init__(self, user_id):
        self.user_id = user_id

        self.courses = {}
        self.courses["course_1"] = Course()

        self.stored_pdf = {}

if __name__ == '__main__':
    a = User('0')
    b = User('1')
    c = User('2')
