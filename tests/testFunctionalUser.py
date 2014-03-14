from django.test import TestCase
from core.models import *
from core.views import *
import random, json
from django.core.handlers.wsgi import *
from django.test.client import Client

class LoginTests(TestCase):
    def setUp(self):
        self.client = Client()

    def postJSON(self, url, data):
        return self.client.post(url, content_type = 'application/json', data=data))

    def testCreateUser(self):
        """
        Tests if user is created
        """
        data = """
            { "username" : "user1", "password" : "pw", "email" : "email@example.com" }
            """
        response = self.postJSON("/users/create", data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('success' in response.content)

    def testLogin(self):
        """
        Tests if login sucessfully
        """
        data = """
            { "username" : "user1", "password" : "pw"
            """
        response = self.postJSON("/users/login", data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('success' in response.content)

    def testInvalidLogin1(self):
        """
        Tests login with invalid username
        """
        data = """
            { "username" : "user2", "password" : "pw"
            """
        response = self.postJSON("/users/login", data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('username' in response.content)

    def testInvalidLogin2(self):
        """
        Tests login with invalid password
        """
        data = """
            { "username" : "user1", "password" : "pw1"
            """
        response = self.postJSON("/users/login", data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('password' in response.content)
