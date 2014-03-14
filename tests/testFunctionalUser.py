from django.test import TestCase
from django.test.client import RequestFactory
from models import *
from views import *
import random, json

class RegistrationTests(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

    # Convenience method to create a POST JSON request
    def postJSON(self, url, data):
        return self.factory.post(url, content_type='application/json', data=data)

    def testNoDuplicates(self):
    	pass

    def testUserGetsCreatedInDatabase(self):
    	pass

    def testUsernameAndPasswordCorrect(self):
    	pass


class ViewUserTests(TestCase):
    def setup(self):
        self.factory = RequestFactory()
        self.testUser = BeatMyGoalUser(username="test", password="test", email="test@test.com")

    def postJSON(self, url, data):
        return self.factory.post(url, content_type='application/json', data=data)

    def testViewUsername(self):
        pass

    def testViewEmail(self):
        pass

class DeleteUserTests(TestCase):
    def setup(self):
        self.factory = RequestFactory()
        self.testUser = BeatMyGoalUser(username="test", password="test", email="test@test.com")

    def postJSON(self, url, data):
        return self.factory.post(url, content_type='application/json', data=data)

    def testDeleteUser(self):
        pass

