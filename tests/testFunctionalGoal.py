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

class GoalPageTests(TestCase):
    def setUp(self):
        BeatMyGoalUser.create("test", "test@test.com", "test")
        self.testUser = BeatMyGoalUser.objects.get(username="test")
        self.client = Client()

    # Convenience method to create a POST JSON request
    def postJSON(self, url, data):
        return self.client.post(url, content_type='application/json', data=data)

    def testCreateGoalPageDoesNotLoadWithoutLoggingIn(self):
        """
        Tests to make sure the create goal page loads
        """

        response = self.client.get("/goals/create", {})
        self.assertEqual(response.status_code, 302) #Must redirect to the index page

    def testValidGoalCreateWithoutLoggingIn(self):
        data = """
        { "title" : "test_title", "description" : "test_description", "prize" : "test_prize",
        "private_setting" : 1, "goal_type" : "Time-based", "ending_value": "50", "unit" : "pound", 
        "ending_date" : "7/6/2014" }
        """
        response = self.postJSON("/goals/create", data)
        self.assertEqual(response.status_code, 302) #Must redirect to the index page

    def testCreateGoalPageLoadWhileLoggingIn(self):
        """
        Tests to make sure the create goal page loads
        """
        data2 = """
        { "username" : "test", "password" : "test" }
        """
        response2 = self.postJSON("/users/login", data2)

        response = self.client.get("/goals/create", {})
        self.assertEqual(response.status_code, 200) #Must redirect to the index page


    def testValidGoalCreateWhileLoggedIn_Timebased(self):
        data = """
        { "title" : "test_title", "description" : "test_description", "prize" : "test_prize",
        "private_setting" : 1, "goal_type" : "Time-based", "ending_value": "50", "unit" : "pound", 
        "ending_date" : "7/6/2014" }
        """
        data2 = """
        { "username" : "test", "password" : "test" }
        """
        response2 = self.postJSON("/users/login", data2)
        response = self.postJSON("/goals/create", data)
        self.assertEqual(response.status_code, 200) #Must redirect to the index page

    def testValidGoalCreateWhileLoggedIn_Valuebased(self):
        data = """
        { "title" : "test_title", "description" : "test_description", "prize" : "test_prize",
        "private_setting" : 1, "goal_type" : "Value-based", "ending_value": "50", "unit" : "pound", 
        "ending_date" : null }
        """
        data2 = """
        { "username" : "test", "password" : "test" }
        """
        response2 = self.postJSON("/users/login", data2)
        response = self.postJSON("/goals/create", data)
        self.assertEqual(response.status_code, 200) #Must redirect to the index page



class ViewGoalTests(TestCase):
    def setUp(self):
        self.client = Client()
        BeatMyGoalUser.create('test','p','wfe@wfewef')
        Goal.create('title','des','test','test_prize', 1, 'Time-based', '50', 'pound', '11/13/2014')

    def postJSON(self, url, data):
        return self.client.post(url, content_type='application/json', data=data)

    def testGoalPageLoads(self):
        """
        Tests to make sure the view page loads
        """        
        response = self.client.get("/goals/1/")
        self.assertEqual(response.status_code, 200)


class EditGoalTests(TestCase):
    def setUp(self):
        self.client = Client()
        BeatMyGoalUser.create("test", "test@test.com", "test")
        self.testUser = BeatMyGoalUser.objects.get(username="test")
        Goal.create('title','des','test','test_prize', 1, 'Time-based', '50', 'pound', '11/13/2014')


    def postJSON(self, url, data):
        return self.client.post(url, content_type='application/json', data=data)

    def testEditGoalPageLoads(self):
        """
        Tests to make sure the edit goal page loads
        """
        data2 = """
        { "username" : "test", "password" : "test" }
        """
        response2 = self.postJSON("/users/login", data2)
        response = self.client.get("/goals/1/edit", {})
        self.assertEqual(response.status_code, 200)


    def testEditGoalSucceeds(self):
       data2 = """
       { "username" : "test", "password" : "test" }
       """
       response2 = self.postJSON("/users/login", data2)

       data = """
       { "title" : "title2", "description" : "des2", "prize" : "100", "ending_value" : "100", "unit" : "pound" }
       """
       response = self.postJSON("/goals/1/edit", data)
       self.assertEqual(response.status_code, 200)

class RemoveGoalTests(TestCase):
    def setUp(self):
        self.testUser = BeatMyGoalUser(username="test", password="test", email="test@test.com")
        self.testUser.save()
        Goal.create('title','des','test','test_prize', 1, 'Time-based', '50', 'pound', '11/13/2014')
        self.testGoal = Goal.objects.get(title='title')
        self.client = Client()

    def postJSON(self, url, data):
        return self.client.post(url, content_type='application/json', data=data)

    def testremoveGoalSucceeds(self):
       data = """
       { "username" : "test", "password" : "test" }
       """
       self.postJSON("/users/login", data)
       data2 = """
       { "goal_id" : %s }
       """ % (self.testGoal.id)
       response2 = self.postJSON("/goals/remove", data2)
       self.assertEqual(response2.status_code, 200)

class JoinGoalTests(TestCase):
    def setUp(self):
        self.client = Client()
        BeatMyGoalUser.create("test", "test@test.com", "test")
        self.testUser = BeatMyGoalUser.objects.get(username="test")
        BeatMyGoalUser.create("test1", "test1@test.com", "test1")
        self.testUser1 = BeatMyGoalUser.objects.get(username='test1')
        Goal.create('title','des','test','test_prize', 1, 'Time-based', '50', 'pound', '11/13/2014')
        self.testGoal = Goal.objects.get(title="title")

    def postJSON(self, url, data):
        return self.client.post(url, content_type='application/json', data=data)

    def testJoinGoalSuccessfully(self):
        data = """
        { "username" : "test1", "password" : "test1" }
        """
        self.postJSON("/users/login", data)
        data2 = """
        {"goal_id" : %s }
        """ % (self.testGoal.id)
        response = self.postJSON("/goals/join", data2)
        json_data = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(json_data['errors'])

    def testJoinNonexistantGoal(self):
        data = """
        { "username" : "test", "password" : "test" }
        """
        self.postJSON("/users/login", data)
        data2 = """
        {"goal_id" : "2" }
        """ 
        response = self.postJSON("/goals/join", data2)
        json_data = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(json_data['errors'])

class LeaveGoalTests(TestCase):
    def setUp(self):
        self.client = Client()
        BeatMyGoalUser.create("test", "test@test.com", "test")
        self.testUser = BeatMyGoalUser.objects.get(username="test")
        BeatMyGoalUser.create("test1", "test1@test.com", "test1")
        self.testUser1 = BeatMyGoalUser.objects.get(username='test1')
        Goal.create('title','des','test','test_prize', 1, 'Time-based', '50', 'pound', '11/13/2014')
        self.testGoal = Goal.objects.get(title="title")

    def postJSON(self, url, data):
        return self.client.post(url, content_type='application/json', data=data)

    def testLeaveGoalSuccessfully(self):
        data = """
        { "username" : "test1", "password" : "test1" }
        """
        self.postJSON("/users/login", data)
        data2 = """
        {"goal_id" : %s }
        """ % (self.testGoal.id)
        self.postJSON("/goals/join", data2)
        response = self.postJSON("/goals/leave", data2)
        json_data = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(json_data['errors'])

    def testNonparticipantLeavesGoal(self):
        data = """
        { "username" : "test1", "password" : "test1" }
        """
        self.postJSON("/users/login", data)
        data2 = """
        {"goal_id" : %s }
        """ % (self.testGoal.id)
        response = self.postJSON("/goals/leave", data2)
        json_data = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(json_data['errors'])


class LogProgressTests(TestCase):
    def setUp(self):
        self.client = Client()
        BeatMyGoalUser.create("test", "test@test.com", "test")
        self.testUser = BeatMyGoalUser.objects.get(username="test")
        Goal.create('title','des','test','test_prize', 1, 'Time-based', '50', 'pound', '11/13/2014')
        self.testGoal = Goal.objects.get(title="title")

    def postJSON(self, url, data):
        return self.client.post(url, content_type='application/json', data=data)

    def testLogProgress(self):
        data = """
        { "username" : "test", "password" : "test" }
        """
        self.postJSON("/users/login", data)
        log = """
        {"amount" : "100", "comment" : "hello world"}
        """
        response = self.postJSON("/goals/" + str(self.testGoal.id) + "/log", log)
        res_json = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(res_json['errors'])


class ImageUploadGoalTests(TestCase):
    def setUp(self):
        self.client = Client()
        BeatMyGoalUser.create("test", "test@test.com", "test")
        self.testUser = BeatMyGoalUser.objects.get(username="test")
        Goal.create('title','des','test','test_prize', 1, 'Time-based', '50', 'pound', '11/13/2014')
        self.testGoal = Goal.objects.get(title="title")

    def postJSON(self, url, data):
        return self.client.post(url, content_type='application/json', data=data)

    def testImageUploadRedirect(self):
        """
        Tests that a goal creator can change profile image and server redirects successfully
        """
        image_path = settings.BASE_DIR + "/tests/microphone.png"
        data = {"image" :open(image_path,"r")}
        response = self.postJSON("/goals/" + str(self.testGoal.id), data)
        self.assertEqual(response.status_code, 301)

    def testImageUploadForm(self):
        """
        Tests that a goal creator can change profile image and Imageform is valid
        """
    
        data= {"image" : SimpleUploadedFile("microphone.png",settings.BASE_DIR + "/tests", content_type = "file")}
        form = ImageForm(self.testGoal.id, data)
        self.assertTrue(form.is_valid())

    def testUserImageUploadFormRequest(self):
        """
        Tests that a user can upload a profile picture through the view
        """
        user_id = str(self.testUser.id)
        image_path = settings.BASE_DIR + "/tests/microphone.png"
        self.assertFalse(BeatMyGoalUser.objects.get(id=user_id).image, "user image empty to start")
        with open(image_path) as fp:
            self.client.post('/users/' + user_id +  '/imageload/', {'image': fp})
        self.assertTrue(BeatMyGoalUser.objects.get(id=user_id).image, "user image is now set")

    def testGoalImageUploadFormRequest(self):
        """
        Tests that a goal can have a photo uploaded through the view
        """
        goal_id = str(self.testGoal.id)
        image_path = settings.BASE_DIR + "/tests/microphone.png"
        self.assertFalse(Goal.objects.get(id=goal_id).image, "goal image empty to start")
        with open(image_path) as fp:
            self.client.post('/goals/' + goal_id +  '/imageload/', {'image': fp})
        self.assertTrue(Goal.objects.get(id=goal_id).image, "user image is now set")

class FavoriteGoalTests(TestCase):
    def setUp(self):
        self.client = Client()
        BeatMyGoalUser.create("test", "test@test.com", "test")
        self.testUser = BeatMyGoalUser.objects.get(username="test")
        Goal.create('title','des','test','test_prize', 1, 'Time-based', '50', 'pound', '11/13/2014')
        self.testGoal = Goal.objects.get(title="title")

    def postJSON(self, url, data):
        return self.client.post(url, content_type='application/json', data=data)

    def testAddFavoriteSuccesfully(self):
        data = """
        { "username" : "test", "password" : "test" }
        """
        self.postJSON("/users/login", data)
        data = """
       { "goal_id" : %s }
       """ % (self.testGoal.id)
        response = self.postJSON("/goals/goal_add_favorite", data)
        json_data = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(json_data['errors'])


    def testRemoveFavoriteSuccesfully(self):
        data = """
        { "username" : "test", "password" : "test" }
        """
        self.postJSON("/users/login", data)
        data = """
       { "goal_id" : %s }
       """ % (self.testGoal.id)
        self.postJSON("/goals/goal_add_favorite", data)
        response = self.postJSON("/goals/goal_remove_favorite", data)
        json_data = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(json_data['errors'])

    def testRemoveFavoritesWhileNotAddedToFavorite(self):
        data = """
        { "username" : "test", "password" : "test" }
        """
        self.postJSON("/users/login", data)
        data = """
       { "goal_id" : %s }
       """ % (self.testGoal.id)
        response = self.postJSON("/goals/goal_remove_favorite", data)
        json_data = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(json_data['errors'])
        self.assertTrue(-210 in json_data['errors'])
        self.assertTrue(-207 in json_data['errors'])




class EmailTests(TestCase):
    def setUp(self):
        self.client = Client()
        BeatMyGoalUser.create("test", "test@test.com", "test")
        self.testUser = BeatMyGoalUser.objects.get(username="test")
        Goal.create('title','des','test','test_prize', 1, 'Time-based', '50', 'pound', '11/13/2014')
        self.testGoal = Goal.objects.get(title="title")

    def postJSON(self, url, data):
        return self.client.post(url, content_type='application/json', data=data)

    def testSendEmailSuccessfully(self):
        data = """
        { "username" : "test", "password" : "test" }
        """
        self.postJSON("/users/login", data)
        data = """
       { "goal_id" : %s, "to" : "kknd113@hotmail.com" }
       """ % (self.testGoal.id)
        response = self.postJSON("/email/", data)
        json_data = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(json_data['errors'])


    def testSendEmailSuccessfullyWithValidAddress(self):
        data = """
        { "username" : "test", "password" : "test" }
        """
        self.postJSON("/users/login", data)
        data = """
       { "goal_id" : %s, "to" : "abc@abc.com" }
       """ % (self.testGoal.id)
        response = self.postJSON("/email/", data)
        json_data = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(json_data['errors'])

    def testSendEmailFailsWithoutValidAdress(self):
        data = """
        { "username" : "test", "password" : "test" }
        """
        self.postJSON("/users/login", data)
        data = """
       { "goal_id" : %s, "to" : "" }
       """ % (self.testGoal.id)
        response = self.postJSON("/email/", data)
        json_data = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(json_data['errors'])
        self.assertTrue(-401 in json_data['errors'])

