from django.test import TestCase
from core.models import *
from core.views import *
from core.constants import *
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
        self.assertTrue(response.status_code < 400)

    def testValidRegistration(self):
        data = """
        { "username" : "jay", "password" : "p", "email" : "email@example.com" }
        """
        response = self.postJSON("/users/create", data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(not json.loads(response.content)['errors'])


class LoginTests(TestCase):
    def setUp(self):
        self.client = Client()
        BeatMyGoalUser.create("user1","email@example.com","pw")


    def postJSON(self, url, data):
        return self.client.post(url, content_type = 'application/json', data=data)

    def testLogin(self):
        """
            Tests if login sucessfully
        """
        data = """
            { "username" : "user1", "password" : "pw"}
        """
        response = self.postJSON("/users/login", data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(not json.loads(response.content)['errors'])
        
    def testInvalidLogin1(self):
        """
            Tests login with invalid username
        """
        data = """
            { "username" : "user2", "password" : "pw"}
        """
        response = self.postJSON("/users/login", data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(CODE_BAD_USERNAME in json.loads(response.content)['errors'])
        
    def testInvalidLogin2(self):
        """
            Tests login with invalid password
        """
        data = """
            { "username" : "user1", "password" : "pw1"}
        """
        response = self.postJSON("/users/login", data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(CODE_BAD_PASSWORD in json.loads(response.content)['errors'])


class ViewUserTests(TestCase):
    def setUp(self):
        self.cleint = Client()
        self.testUser = BeatMyGoalUser(username="kyle", password="123", email="kyle@test.com")
        self.testUser.save()

    def testUserView(self):
        """
        Tests to make sure the view page loads
        """
        userid = self.testUser.id
        username = self.testUser.username
        email = self.testUser.email
        response = self.client.get("/users/" + str(userid)+ "/", {})
        self.assertEqual(response.status_code, 200)


class DeleteUserTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.testUser = BeatMyGoalUser(username="kyle", password="123", email="kyle@test.com")
        self.testUser.save()

    def postJSON(self, url, data):
        return self.client.post(url, content_type='application/json', data=data)

    def testDeleteUser(self):
        """
        Tests that a user can be delete User if logged in
        """
        data = """
        { "username" : "kyle", "password" : "123" }
        """
        response = self.postJSON("/users/login", data)
        response2 = self.postJSON("/users/" + str(self.testUser.id) + "/delete", {})
        self.assertEqual(response2.status_code, 200)


    def testDeleteWrong(self):
        """
        Tests that a user cannot be delete if not logged in
        """
        response = self.postJSON("/users/" + str(self.testUser.id) +"/delete", {})
        self.assertEqual(response.status_code, 500)

    

class EditUserTests(TestCase):
    def setUp(self):
        self.cleint = Client()
        self.testUser = BeatMyGoalUser(username="test", password="test", email="test@test.com")
        self.testUser.save()

    def postJSON(self, url, data):
        return self.client.post(url, content_type='application/json', data=data)

    def testEditUser(self):
        """
        Tests that a user can be edited if logged in
        """
        data = """
        { "username" : "test", "password" : "test" }
        """
        response = self.postJSON("/users/login", data)
        data2 = """
        {"username" : "test1", "email" : "newemail@email.com"}
        """
        response2 = self.postJSON("/users/1/edit", data2)
        self.assertEqual(response2.status_code, 200)
        self.assertTrue(not json.loads(response2.content)['errors'])

    def testEditWrongUser(self):
        """
        Tests that a user cannot be edited if not logged in
        """
        data2 = """
        {"username" : "test1", "email" : "newemail@email.com"}
        """
        response2 = self.postJSON("/users/1/edit", data2)
        self.assertEqual(response2.status_code, 500)
