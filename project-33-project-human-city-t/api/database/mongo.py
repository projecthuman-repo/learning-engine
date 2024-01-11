from typing import List, Tuple, Optional
import certifi
from mongoengine import Document, StringField, EmailField, IntField, ListField, DateTimeField, FloatField, ObjectIdField, connect
from bson import ObjectId
import random
import string


mongo_uri = open('api/database/mongodb_uri', 'r').read()
connect(host=mongo_uri, tlsCAFile=certifi.where())


class User(Document):
    UserID = StringField(primary_key=True)
    Name = StringField(required=True)
    Email = EmailField(required=True, unique=True)
    Password = StringField(required=True)
    Role = StringField(choices=["Educator", "Learner"])
    ExperienceLevel = StringField()
    TotalScore = IntField()
    LearningTrackRecord = ListField(StringField())
    LastLogin = DateTimeField()
    AccountType = StringField()
    Country = StringField()
    School = StringField()
    StateProvince = StringField()

    meta = {
        'collection': 'APIUser'
    }

class Course(Document):
    CourseID = StringField(primary_key=True)
    CourseName = StringField(required=True)
    CourseCategory = StringField(required=True)
    CourseDescription = StringField(required=True)
    StartDate = DateTimeField()
    EndDate = DateTimeField()
    EducatorID = StringField()
    Rating = FloatField()
    Reviews = ListField(StringField())
    CourseDifficulty = StringField()

    meta = {
        'collection': 'courses' 
    }

class Material(Document):
    CourseID = StringField(required=True)
    MaterialType = StringField(required=True)
    MaterialContent = StringField(required=True)
    AccessType = StringField(required=True)
    HighlightedText = ListField(StringField())
    MaterialDifficulty = StringField()

    meta = {
        'collection': 'learningmaterials' 
    }

class Game(Document):
    CourseID = StringField(required=True)
    GameType = StringField(required=True)
    GameContent = StringField(required=True)
    MaterialID = ObjectIdField(required=True)

    meta = {
        'collection': 'games' 
    }

class Auth(Document):
    Name = StringField(primary_key=True)
    Token = StringField()

    meta = {
        'collection': 'userauth'
    }


def getMaterial(materialID: str) -> Optional[Tuple[str, str, List[str]]]:
    """
        This method gets the material for the Course
    
        Returns:
            None: if there is no material for the course
            str:  returns material with relevant course id 
        """
    if materials := Material.objects(id=materialID):
        return (materials[0].MaterialContent, materials[0].MaterialDifficulty, materials[0].HighlightedText)
    return None

def createMaterial(courseId: str, courseMaterial: str, courseDifficulty: str, materialType: str, accessType: str, highlightedText: list[str]) -> int:
    """
    This method inserts material for a specific course

    Returns:
        int: returns id of inserted material
    """
    new_material = Material(CourseID = courseId, MaterialType = materialType, MaterialContent = courseMaterial, AccessType = accessType, MaterialDifficulty = courseDifficulty, HighlightedText=highlightedText)
    return new_material.save().id

def getGame(gameID) -> Optional[Tuple[str, str, str]]:
    """
    This method returns content of game of gameType for a specific course and its specific material 

    Returns:
        str: returns content of game if game exists
        None:  returns none if game doesnt exists
    """
    for game in Game.objects(id=gameID):
        if game:
            return game.GameContent, game.GameType, game.MaterialID
    return None

def createGame(courseId: str, gameType: str, gameContent: str, materialId: str) -> int:
    """
    This method inserts content of game of gameType for a specific course and its specific material 

    Returns:
        int: returns id of inserted game
    """
    
    new_game = Game(CourseID = courseId, GameType = gameType, GameContent = gameContent, MaterialID = ObjectId(materialId))
    return new_game.save().id

def checkPassword(userName: str, pwd: str) -> Optional[bool]:
    """
    This method returns true if correctly authenticated.
    Returns:
        True: if username and password provided is correct
        False:  if username and password provided is incorrect
    """
    for user in User.objects():
        if user.Name == userName :
            return user.Password == pwd
    return False

def checkUsername(userName: str) -> Optional[bool]:
    for user in User.objects():
        if user.Name == userName :
            return True
    return False

def isAdmin(userName: str) -> Optional[str]:
    for user in User.objects():
        if user.Name == userName :
            return user.AccountType == "Admin"
    return False

def generateToken(userName: str) -> Optional[str]:
    token = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

    for user in Auth.objects(Name=userName):
        user.Token = token
        user.save()
        return token

    record = Auth(Name = userName, Token = token)
    record.save()
    return token

def verifyToken(token: str) -> bool:
    for auth in Auth.objects(Token=token):
        if auth:
            return True
    return False