from core.models import Goal, BeatMyGoalUser
from core.constants import *
import unittest
from django.test import TestCase
from django.contrib.auth.models import User


class CreateLoginUserTest(unittest.TestCase):
    def setUp(self):
        BeatMyGoalUser.objects.all().delete()
        Goal.objects.all().delete()
    
    def testCreateUser(self):
        """
        Tests that creating new user works
        """
        response = BeatMyGoalUser.create('user1', 'email1@gmail.com', 'pw')
        self.assertTrue(not response['errors'])
        userid = BeatMyGoalUser.objects.get(username = 'user1')
        self.assertEqual('email1@gmail.com', userid.email)

        # We are storing passwords as hashs now.
        # self.assertEqual('pw', userid.password)


    def testCreateDuplicateUser(self):
        """
        Tests that creating account with already existing username works
        """
        response1 = BeatMyGoalUser.create('user1', 'email1@gmail.com', 'pw')
        self.assertTrue(not response1['errors'])
        response2 = BeatMyGoalUser.create('user1', 'email2@gmail.com', 'pw')
        self.assertTrue(response2['errors'])
        self.assertTrue(CODE_DUPLICATE_USERNAME in response2['errors'])
        self.assertFalse(CODE_DUPLICATE_EMAIL in response2['errors'])
    
    def testCreateDuplicateEmail(self):
        """
        Tests that creating account with already existing email works
        """
        response1 = BeatMyGoalUser.create('user1', 'email1@gmail.com', 'pw')
        self.assertTrue(not response1['errors'])
        response2 = BeatMyGoalUser.create('user2', 'email1@gmail.com', 'pw')
        self.assertTrue(response2['errors'])
        self.assertFalse(CODE_DUPLICATE_USERNAME in response2['errors'])
        self.assertTrue(CODE_DUPLICATE_EMAIL in response2['errors'])
            
    def testCreateEmptyUsername(self):
        """
        Tests that creating account with empty username
        """
        response = BeatMyGoalUser.create('', 'email1@gmail.com', 'pw')
        self.assertTrue(response['errors'])

    def testCreateEmptyEmail(self):
        """
        Tests that creating account with empty email
        """
        response = BeatMyGoalUser.create('user1', '', 'pw')
        self.assertTrue(response['errors'])

    def testCreateEmptyPassword(self):
        """
        Tests that creating account with empty password
        """
        response = BeatMyGoalUser.create('user1', 'email1@gmail.com', '')
        self.assertTrue(response['errors'])

    def testLoginUser(self):
        """
        Tests login with registered username
        """
        BeatMyGoalUser.create('user1', 'email1@gmail.com', 'pw')
        response = BeatMyGoalUser.login('user1', 'pw')
        self.assertTrue(not response['errors'])

    def testLoginInvalidUser(self):
        """
        Tests login with unregistered username
        """
        response = BeatMyGoalUser.login('user1','pw')
        self.assertTrue(response['errors'])

    def testLoginInvalidPassword(self):
        """
        Tests login with wrong password
        """
        BeatMyGoalUser.create('user1', 'email1@gmail.com', 'pw')
        response = BeatMyGoalUser.login('user1','pww')
        self.assertTrue(response['errors'])


class ViewUserTest(unittest.TestCase):
    def setUp(self):
        BeatMyGoalUser.objects.all().delete()
        Goal.objects.all().delete()
    

    def testGetUserbyId(self):
        """
        test getUserById method in models
        """
        responce = BeatMyGoalUser.create('test_user_view','test_email_view','test_password_view')
        test_user = responce['user']
        test_user_userid = test_user.id
        test_user_username = test_user.username
        test_user_email = test_user.email
        response = BeatMyGoalUser.getUserById(test_user_userid)
        self.assertTrue(not response['errors'])
        user = response['user']
        self.assertEqual(test_user_userid,user.id)
        self.assertEqual(test_user_username,user.username)
        self.assertEqual(test_user_email,user.email)

    
    def testGetUserbyName(self):
        """
        test getUserByName method in models
        """
        responce = BeatMyGoalUser.create('test_user_view','test_email_view','test_password_view')
        test_user = responce['user']
        test_user_userid = test_user.id
        test_user_username = test_user.username
        test_user_email = test_user.email
        response = BeatMyGoalUser.getUserByName(test_user_username)
        self.assertTrue(not response['errors'])
        user = response['user']
        self.assertEqual(test_user_userid,user.id)
        self.assertEqual(test_user_username,user.username)
        self.assertEqual(test_user_email,user.email)

    def testGetUserbyIdWrong(self):
        """
        test getUserByName method in models
        """
        response = BeatMyGoalUser.getUserById(-99)
        self.assertTrue(response['errors'])

    def testGetUserbyNameWrong(self):
        """
        test getUserByName method in models
        """
        response = BeatMyGoalUser.getUserByName("")
        self.assertTrue(response['errors'])

    def testRemoveUser(self):
        """
        test delete method in models
        """
        response = BeatMyGoalUser.create('test_user_view','test_email_view','test_password_view')
        test_user = response['user']
        test_user_userid = test_user.id
        response1 = BeatMyGoalUser.remove(test_user_userid)
        self.assertTrue(not response1['errors'])
        response2 = BeatMyGoalUser.getUserById(test_user_userid)
        self.assertTrue(response2['errors'])

    def testRemoveUserWrong(self):
        """
        test delete method in models
        """
        response = BeatMyGoalUser.remove(-99)
        self.assertTrue(response['errors'])


class EditUserTests(TestCase):
    def setUp(self):
        self.testUser = BeatMyGoalUser(username="test", password="test", email="test@test.com")
        self.testUser.save()
        self.testUser1 = BeatMyGoalUser(username="test1", password="test1", email="test1@test1.com")
        self.testUser1.save()

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
    


