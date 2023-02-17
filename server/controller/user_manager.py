import server.models.UserData.user_data_classes as udc



class UserManager:
    def __init__(self):
        # load user placeholder
        users = {}
        users["1"] = udc.User('0')
