from core.models import Goal, BeatMyGoalUser
from core.views import user_login_fb
from core.constants import *
import unittest
from django.test import TestCase
from django.contrib.auth.models import *
from django.test.client import RequestFactory

class MockFacebookUser():
    def __init__(self, name, email, id):
        self.name = None
        self.email = None
        self.id = None
        self.stored = (name, email, id)

    def update(self):
        self.name, self.email, self.id = self.stored
        
class MockFacebookRequest():
    def __init__(self, name, email, id):
        self.user = MockFacebookUser(name, email, id)
        self.error = False
        
class FacebookUserLoginTest(unittest.TestCase):
    def setUp(self):
        self.fb_mock = MockFacebookRequest("Name", "email", 10)
        self.factory = RequestFactory()

        self.request = self.factory.get("/users/login/fb")
        self.request.user = AnonymousUser()
        self.request.session = {}
        
        BeatMyGoalUser.objects.all().delete()
 
    def testFacebookCreate(self):
        """
        Tests that creating a Facebook user works
        """
        user_login_fb(self.request, self.fb_mock)
        self.fb_mock.user.update()
        self.assertTrue(BeatMyGoalUser.objects.filter(username=self.fb_mock.user.name).exists(), "facebook user exists in db")

    def testFacebookLogin(self):
        """
        Tests that logging in a Facebook user works
        """
        prev_count = BeatMyGoalUser.objects.count()
        self.fb_mock.user.update()
        user_login_fb(self.request, self.fb_mock)
        self.assertEqual(prev_count + 1, BeatMyGoalUser.objects.count(), "new fb user created")
        user_login_fb(self.request, self.fb_mock)
        self.assertEqual(prev_count + 1, BeatMyGoalUser.objects.count(), "existing fb user logged in")

        

