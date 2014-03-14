from django.test import TestCase
from core.models import *
from core.views import *
import random, json
from django.core.handlers.wsgi import *
from django.test.client import Client

class RegistrationTests(TestCase):

    def setUp(self):
        self.client = Client()

    # Convenience method to create a POST JSON request
    def postJSON(self, url, data):
        return self.client.post(url, content_type='application/json', data=data)

    def testRegistrationPageLoads(self):
        """
        Tests to make sure the registration page loads
        """
        response = self.client.get("/users/create", {})
        self.assertEqual(response.status_code, 200)

    def testValidRegistration(self):
        data = """
        { "username" : "jay", "password" : "p", "email" : "email@example.com" }
        """
        response = self.postJSON("/users/create", data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('success' in response.content)


class ViewUserTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.testUser = BeatMyGoalUser(username="test", password="test", email="test@test.com")

    def postJSON(self, url, data):
        return self.client.post(url, content_type='application/json', data=data)

    def testViewPageLoads(self):
        """
        Tests to make sure the view page loads
        """
        response = self.client.get("/users/1/")
        self.assertEqual(response.status_code, 200)


class DeleteUserTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.testUser = BeatMyGoalUser(username="test", password="test", email="test@test.com")

    def postJSON(self, url, data):
        return self.client.post(url, content_type='application/json', data=data)

    def testDeleteUser(self):
        pass
