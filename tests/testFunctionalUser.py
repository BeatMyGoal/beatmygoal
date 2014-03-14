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

# Create your tests here

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



class EditUserTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.testUser = BeatMyGoalUser(username="test", password="test", email="test@test.com")
        self.testUser.save()
        self.testUser1 = BeatMyGoalUser(username="test1", password="test1", email="test1@test1.com")
        self.testUser1.save()

    def postJSON(self, url, data):
        return self.factory.post(url, content_type="application/json", data=data)

    def testEditUsername(self):
        BeatMyGoalUser.updateUser(user=self.testUser, username="newUsername")
        self.assertEqual(self.testUser.username, "newUsername")

    def testEditEmail(self):
        BeatMyGoalUser.updateUser(user=self.testUser, email="newemail@email.com")
        self.assertEqual(self.testUser.email, "newemail@email.com")

    def testUsernameTaken(self):
        BeatMyGoalUser.updateUser(user=self.testUser, username="test1")
        self.assertEqual(self.testUser.username, "test")

    def testEmailTaken(self):
        BeatMyGoalUser.updateUser(user=self.testUser, email="test1@test1.com")
        self.assertEqual(self.testUser.email, "test@test.com")

    def testUserIsAuthenticated(self):
        pass
