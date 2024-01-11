import unittest
import sys
sys.path.append('../routers/')
import api.database.game_api_db as game_api_db
from flask import json


class TestGetMaterialEndpoint(unittest.TestCase):
    def setUp(self):
        self.app = game_api_db.app.test_client()
        self.app.testing = True

    def testGetMaterialWithValidCourseId(self):
        response = self.app.get('/material/get?courseId=course123')  
        data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 200)
        self.assertIn('Content', data)

    def testGetMaterialWithInvalidCourseId(self):
        response = self.app.get('/material/get?courseId=1234')  
        data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 404)
        self.assertIn('error', data)
        self.assertEqual(data['error'], 'Not Found: Value not found')

    def testGetMaterialWithNonexistentCourseId(self):
        response = self.app.get('/material/get?courseId=')  
        data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 400)
        self.assertIn('error', data)
        self.assertEqual(data['error'], 'Bad Request: Invalid value')

class TestInsertMaterialEndpoint(unittest.TestCase):
    def setUp(self):
        self.app = game.app.test_client()
        self.app.testing = True

    def testMaterialCreationWithInvalidParameters(self):
        
        headersInput = {
            'accept': 'application/json',
            'Content-Type': 'application/json',
        }

        dataInput = {
            "accessType": "string",
            "courseDifficulty": "string",
            "courseId": "course12344",
            "materialType": "string"
        }

        response = self.app.post('/material/create', headers=headersInput, data=dataInput)


        data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 400)
        self.assertIn('error', data)
        self.assertEqual(data['error'], 'Bad Request: Invalid value')


if __name__ == '__main__':
    unittest.main()