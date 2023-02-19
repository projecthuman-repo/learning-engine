
import server.models.UserData.user_data_classes as udc
class UserManager:
    def __init__(self):
        # load user placeholder
        self.user_dict = {}

    def create_tf_game(self, user_id: str, course_title: str, module_title: str,
                       concept_title: str, data):
        local_game_id = self.user_dict[user_id].courses[course_title].modules[module_title].\
            concepts[concept_title].local_game_id_counter["TF"]
        self.user_dict[user_id].courses[course_title].modules[module_title]. \
            concepts[concept_title].local_game_id_counter["TF"] += 1

        game = udc.TrueOrFalseGame(concept_title, local_game_id, data)

        self.user_dict[user_id].courses[course_title].modules[module_title].\
            concepts[concept_title].games["TF"][local_game_id] = game
    def update_tf_game(self,user_id: str, course_title: str, module_title: str,
                    concept_title: str, data, game_id):

        game = udc.TrueOrFalseGame(concept_title, game_id, data)

        self.user_dict[user_id].courses[course_title].modules[module_title].\
            concepts[concept_title].games["TF"][game_id] = game

    def create_concept(self,user_id:str, course_title: str, module_title:str, concept_title:str):
        self.user_dict[user_id].courses[course_title].modules[module_title].concepts[concept_title]\
            = udc.Concept()
    def create_module(self,user_id:str, course_title: str, module_title:str):
        self.user_dict[user_id].courses[course_title].modules[module_title] = udc.Module()
    def create_course(self,user_id:str, course_title:str):
        self.user_dict[user_id].courses[course_title] = udc.Course()
