from abc import ABC, abstractmethod
import threading


class Game(ABC):
    def __init__(self, concept_tag: str, game_id):
        self.data = None
        self.concept_tag = concept_tag
        self.game_type = None
        self.game_id = game_id

    def get_data(self):
        return self.data


class TrueOrFalseGame(Game):
    def __init__(self, concept_tag: str, game_id: str, data):
        super().__init__(concept_tag, game_id)
        self.game_type = "TF"
        self.data = data
        # t = threading.Thread(target=self.init_BoolQGen(payload))
        # t.start()


class Concept():
    def __init__(self):
        self.games = {"TF": {}, "MCQ": {}, "CW": {}, "WS": {}, "MW": {}, "FIB": {}}
        self.local_game_id_counter = {"TF": 0, "MCQ": 0, "CW": 0, "WS": 0, "MW": 0, "FIB": 0}

class Module():
    def __init__(self):
        self.concepts = {}




class Course():
    def __init__(self):
        self.modules = {}


class User():
    def __init__(self, user_id):
        self.user_id = user_id

        self.courses = {}

        self.stored_pdf = {}


if __name__ == '__main__':
    a = User('0')
    b = User('1')
    c = User('2')
