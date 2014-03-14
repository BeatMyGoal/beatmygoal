from django.test import TestCase
from django.test.client import RequestFactory
from core.models import *
from core.views import *
import random, json

class GoalFunctionalTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

    # Convenience method to create a POST JSON request
    def postJSON(self, url, data):
        return self.factory.post(url, content_type='application/json', data=data)



