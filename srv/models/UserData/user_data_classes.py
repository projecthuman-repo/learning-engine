from abc import ABC, abstractmethod
import threading


class Game():
    def __init__(self, concept_tag: str, game_id, data, game_type):
        self.data = None
        self.concept_tag = concept_tag
        self.game_type = game_type
        self.game_id = game_id
        self.data = data

    def get_data(self):
        return self.data

class TrueOrFalseGame(Game):
    def __init__(self, concept_tag: str, game_id: str, data):
        super().__init__(concept_tag, game_id)
        self.game_type = "TF"
        self.data = data
        # t = threading.Thread(target=self.init_BoolQGen(payload))
        # t.start()
class MultipleChoiceGame(Game):
    def __init__(self, concept_tag: str, game_id: str, data):
        super().__init__(concept_tag, game_id)
        self.game_type = "MC"
        self.data = data

class WordSearchGame(Game):
    def __init__(self, concept_tag: str, game_id: str, data):
        super().__init__(concept_tag, game_id)
        self.game_type = "WS"
        self.data = data

class FillInTheBlankGame(Game):
    def __init__(self, concept_tag: str, game_id: str, data):
        super().__init__(concept_tag, game_id)
        self.game_type = "FITB"
        self.data = data

class CrosswordGame(Game):
    def __init__(self, concept_tag: str, game_id: str, data):
        super().__init__(concept_tag, game_id)
        self.game_type = "CW"
        self.data = data

class DefinitionMatchGame(Game):
    def __init__(self, concept_tag: str, game_id: str, data):
        super().__init__(concept_tag, game_id)
        self.game_type = "DM"
        self.data = data


class Concept():
    def __init__(self):
        self.games = {"TF": {}, "MC": {}, "CW": {}, "WS": {}, "DM": {}, "FITB": {}}
        self.local_game_id_counter = {"TF": 0, "MC": 0, "CW": 0, "WS": 0, "DM": 0, "FITB": 0}

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
