from django.test import TestCase
from core.models import *
from core.views import *
from core.constants import *
import random, json
from django.core.handlers.wsgi import *
from django.test.client import Client

class GoalPageTests(TestCase):

    def setUp(self):
        self.testUser = BeatMyGoalUser(username="test", password="test", email="test@test.com")
        self.testUser.save()
        self.client = Client()

    # Convenience method to create a POST JSON request
    def postJSON(self, url, data):
        return self.client.post(url, content_type='application/json', data=data)

    def testCreateGoalPageDoesNotLoadWithoutLoggingIn(self):
        """
        Tests to make sure the create goal page loads
        """

        response = self.client.get("/goals/create", {})
        self.assertEqual(response.status_code, 302) #Must redirect to the index page

    def testValidGoalCreateWithoutLoggingIn(self):
        data = """
        { "title" : "test_title", "description" : "test_description", "prize" : "test_prize",
        "private_setting" : 1, "goal_type" : "test_goal_type" }
        """
        response = self.postJSON("/goals/create", data)
        self.assertEqual(response.status_code, 302) #Must redirect to the index page



    def testCreateGoalPageLoadWhileLoggingIn(self):
        """
        Tests to make sure the create goal page loads
        """
        data2 = """
        { "username" : "test", "password" : "test" }
        """
        response2 = self.postJSON("/users/login", data2)

        response = self.client.get("/goals/create", {})
        self.assertEqual(response.status_code, 200) #Must redirect to the index page

    def testValidGoalCreateWhileLoggedIn(self):
        data = """
        { "title" : "test_title", "description" : "test_description", "prize" : "test_prize",
        "private_setting" : 1, "goal_type" : "test_goal_type" }
        """
        data2 = """
        { "username" : "test", "password" : "test" }
        """
        response2 = self.postJSON("/users/login", data2)

        response = self.postJSON("/goals/create", data)
        self.assertEqual(response.status_code, 200) #Must redirect to the index page



class ViewGoalTests(TestCase):
    def setUp(self):
        self.client = Client()
        #self.testUser = BeatMyGoalUser(username="test", password="test", email="test@test.com")
        #self.testGoal = Goal.objects.create('title','des','test','test_prize', 1, 'test_type')
        BeatMyGoalUser.create('test','p','wfe@wfewef')
        Goal.create('title','des','test','test_prize', 1, 'test_type')

    def postJSON(self, url, data):
        return self.client.post(url, content_type='application/json', data=data)

    def testGoalPageLoads(self):
        """
        Tests to make sure the view page loads
        """        
        response = self.client.get("/goals/1/")
        self.assertEqual(response.status_code, 200)


class EditGoalTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.testUser = BeatMyGoalUser(username="test", password="test", email="test@test.com")
        self.testUser.save()
        Goal.create('title','des','test','test_prize', 1, 'test_type')


    def postJSON(self, url, data):
        return self.client.post(url, content_type='application/json', data=data)

    def testEditGoalPageLoads(self):
        """
        Tests to make sure the edit goal page loads
        """
        data2 = """
        { "username" : "test", "password" : "test" }
        """
        response2 = self.postJSON("/users/login", data2)


        response = self.client.get("/goals/1/edit", {})
        self.assertEqual(response.status_code, 200)


    def testEditGoalSucceeds(self):
       data2 = """
       { "username" : "test", "password" : "test" }
       """
       response2 = self.postJSON("/users/login", data2)

       data = """
       { "title" : "title2", "description" : "des2", "password" : "test"}
       """
       response = self.postJSON("/goals/1/edit", data)
       self.assertEqual(response.status_code, 200)

class RemoveGoalTests(TestCase):
    def setUp(self):
        self.testUser = BeatMyGoalUser(username="test", password="test", email="test@test.com")
        self.testUser.save()
        Goal.create('title','des','test','test_prize', 1, 'test_type')
        self.testGoal = Goal.objects.get(title='title')


    def postJSON(self, url, data):
        return self.client.post(url, content_type='application/json', data=data)

    def testremoveGoalSucceeds(self):
       data = """
       { "username" : "test", "password" : "test" }
       """
       self.postJSON("/users/login", data)
       data2 = """
       { "goal_id" : %s }
       """ % (self.testGoal.id)
       response2 = self.postJSON("/goals/remove", data2)
       self.assertEqual(response2.status_code, 200)

