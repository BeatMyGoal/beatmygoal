from django.test import TestCase
from core.models import *
from core.views import *
from core.constants import *
import random, json
from django.core.handlers.wsgi import *
from django.test.client import Client

class FavoriteGoalTests(TestCase):
    def setUp(self):
        self.client = Client()
        BeatMyGoalUser.create("test", "test@test.com", "test")
        self.testUser = BeatMyGoalUser.objects.get(username="test")
        Goal.create('title','des','test','test_prize', 1, 'Time-based', '50', 'pound', '11/13/2014')
        self.testGoal = Goal.objects.get(title="title")

    def postJSON(self, url, data):
        return self.client.post(url, content_type='application/json', data=data)

    def testAddFavoriteSuccesfully(self):
        data = """
        { "username" : "test", "password" : "test" }
        """
        self.postJSON("/users/login", data)
        data = """
       { "goal_id" : %s }
       """ % (self.testGoal.id)
        response = self.postJSON("/goals/goal_add_favorite", data)
        json_data = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(json_data['errors'])


    def testRemoveFavoriteSuccesfully(self):
        data = """
        { "username" : "test", "password" : "test" }
        """
        self.postJSON("/users/login", data)
        data = """
       { "goal_id" : %s }
       """ % (self.testGoal.id)
        self.postJSON("/goals/goal_add_favorite", data)
        response = self.postJSON("/goals/goal_remove_favorite", data)
        json_data = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(json_data['errors'])

    def testRemoveFavoritesWhileNotAddedToFavorite(self):
        data = """
        { "username" : "test", "password" : "test" }
        """
        self.postJSON("/users/login", data)
        data = """
       { "goal_id" : %s }
       """ % (self.testGoal.id)
        response = self.postJSON("/goals/goal_remove_favorite", data)
        json_data = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(json_data['errors'])
        self.assertTrue(-210 in json_data['errors'])
        self.assertTrue(-207 in json_data['errors'])