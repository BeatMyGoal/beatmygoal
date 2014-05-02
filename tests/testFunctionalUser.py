from django.test import TestCase
from core.models import *
from core.views import *
from core.constants import *
import random, json
from django.core.handlers.wsgi import *
from django.test.client import Client
from django.core.files.uploadedfile import SimpleUploadedFile
from core.forms import *
from django.conf import settings

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

    def testLogout(self):
        """
        Tests logging out after logging in
        """
        data = """
            { "username" : "user1", "password" : "pw"}
        """
        response = self.postJSON("/users/login", data)
        self.assertEqual(response.status_code, 200)
        response = self.client.get("/users/logout", {})
        self.assertEqual(response.status_code, 302, "redirecting home")        

    def testConfirm(self):
        """
        Tests confirming which is required for reauth
        """
        data = """
            { "username" : "user1", "password" : "pw"}
        """
        response = self.postJSON("/users/login", data)
        self.assertEqual(response.status_code, 200)
        response = self.postJSON("/confirm", data)
        self.assertEqual(response.status_code, 200)


class ViewUserTests(TestCase):
    def setUp(self):
        self.client = Client()
        BeatMyGoalUser.create("kyle", "kyle@test.com", "123")
        self.testUser = BeatMyGoalUser.objects.get(username="kyle")

    def postJSON(self, url, data):
        return self.client.post(url, content_type='application/json', data=data)

    def testUserView(self):
        """
        Tests to make sure the view page loads
        """
        userid = self.testUser.id
        username = self.testUser.username
        email = self.testUser.email
        response = self.client.get("/users/" + str(userid)+ "/", {})
        self.assertEqual(response.status_code, 200)

    def testUserProfileLoggedIn(self):
        """
        Tests when a user loads their own profile
        """
        data = """
        { "username" : "kyle", "password" : "123" }
        """
        response = self.postJSON("/users/login", data)
        response2 = self.client.get("/users/profile", {})
        self.assertEqual(response2.status_code, 302)
        self.assertTrue("/users/" + str(self.testUser.id)+ "/" in str(response2), 
                        "redirect to profile")

    def testUserProfileNotLoggedIn(self):
        """
        Tests when a user tries to load their own profile and not logged in
        """
        response2 = self.client.get("/users/profile", {})
        self.assertEqual(response2.status_code, 302)
        self.assertTrue("/users/create/" in str(response2), 
                        "redirect to create an account")



class DeleteUserTests(TestCase):
    def setUp(self):
        self.client = Client()
        BeatMyGoalUser.create("kyle", "kyle@test.com", "123")
        self.testUser = BeatMyGoalUser.objects.get(username="kyle")

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
        self.client = Client()
        BeatMyGoalUser.create("test", "test@test.com", "test")
        self.testUser = BeatMyGoalUser.objects.get(username="test")

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
        {"username" : "test1", "email" : "newemail@email.com", "password" : "test"}
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

class ImageUploadUserTests(TestCase):
    def setUp(self):
        self.client = Client()
        BeatMyGoalUser.create("test", "test@test.com", "test")
        self.testUser = BeatMyGoalUser.objects.get(username="test")

    def postJSON(self, url, data):
        return self.client.post(url, content_type='application/json', data=data)

    def testImageUploadRedirect(self):
        """
        Tests that a user can change profile image and server redirects successfully 
        """
        image_path = settings.BASE_DIR + "/tests/microphone.png"
        data = {"image" :open(image_path,"r")}
        response = self.postJSON("/users/" + str(self.testUser.id), data)
        self.assertEqual(response.status_code, 301)
    
    def testImageUploadForm(self):
        """
        Tests that a user can change profile image and Imageform is valid
        """

        data= {"image" : SimpleUploadedFile("microphone.png",settings.BASE_DIR + "/tests", content_type = "file")}
        form = ImageForm(self.testUser, data)
        self.assertTrue(form.is_valid())

class HomepageTests(TestCase):
    def setUp(self):
        self.client = Client()
        BeatMyGoalUser.create("kyle", "kyle@test.com", "123")
        self.testUser = BeatMyGoalUser.objects.get(username="kyle")

    def postJSON(self, url, data):
        return self.client.post(url, content_type='application/json', data=data)

    def testIndexLoggedIn(self):
        """
        Tests index if a user is logged in
        """
        data = """
        { "username" : "kyle", "password" : "123" }
        """
        response = self.postJSON("/users/login", data)
        response2 = self.client.get("/", {})
        self.assertEqual(response2.status_code, 302)
        self.assertTrue("/dashboard/" in str(response2), 
                        "redirect to dashboard")

    def testIndexNotLoggedIn(self):
        """
        Tests index if a user is not logged in
        """
        response2 = self.client.get("/", {})
        self.assertEqual(response2.status_code, 200)
