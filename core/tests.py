from django.test import TestCase
from django.test.client import RequestFactory
import models, views
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
