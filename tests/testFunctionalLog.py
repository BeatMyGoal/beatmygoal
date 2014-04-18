from django.test import TestCase
from core.models import *
from core.views import *
from core.constants import *
import random, json
from django.core.handlers.wsgi import *
from django.test.client import Client

class LogTests(TestCase):

    def setUp(self):
        self.client = Client()
        BeatMyGoalUser.create("user1","email@example.com","pw")
        Goal.create('title','des','user1','test_prize', 1, 'Time-based', '50', 'pound', '11/13/2014')
        self.testGoal = Goal.objects.get(title="title")


    # Convenience method to create a POST JSON request
    def postJSON(self, url, data):
        return self.client.post(url, content_type='application/json', data=data)

    def testLogProgress(self):
        data = """
            { "username" : "user1", "password" : "pw"}
        """
        self.postJSON("/users/login", data)
        data = """
        {"goal_id" : %s }
        """ % (self.testGoal.id)
        self.postJSON("/goals/join", data)
        data = {
            "comment" : "hello world",
            "amount" : 20,
        }
        res = json.loads(self.postJSON("/goals/" + str(self.testGoal.id) + "/log", json.dumps(data)).content)
        self.assertFalse(res['errors'])