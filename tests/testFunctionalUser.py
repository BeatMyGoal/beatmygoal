from django.test import TestCase
from django.test.client import RequestFactory
from core.models import *
from core.views import *
import random, json

class RegistrationTests(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

    # Convenience method to create a POST JSON request
    def postJSON(self, url, data):
        return self.factory.post(url, content_type='application/json', data=data)

    def testRegistrationPageLoads(self):
        """
        Tests to make sure the registration page loads
        """
        request = self.factory.get("/users/create")
        response = create_user(request)
        self.assertEqual(response.status_code, 200)
        #print response

    def testValidRegistration(self):
    	pass

    def testInvalidRegistration(self):
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

