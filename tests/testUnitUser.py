from core.models import Goal, BeatMyGoalUser
import unittest
from django.test import TestCase
from django.contrib.auth.models import User


class User_Create_Login_Test(unittest.TestCase):
    def setUp(self):
        BeatMyGoalUser.objects.all().delete()
        Goal.objects.all().delete()
    
    def testCreateUser(self):
        """
        Tests that creating new user works
        """
        response = BeatMyGoalUser.create('user1', 'email1@gmail.com', 'pw')
        self.assertTrue('success' in response)
        userid = BeatMyGoalUser.objects.get(username = 'user1')
        self.assertEqual('email1@gmail.com', userid.email)
        self.assertEqual('pw', userid.password)

    def testCreateDuplicateUser(self):
        """
        Tests that creating account with already existing username works
        """
        response1 = BeatMyGoalUser.create('user1', 'email1@gmail.com', 'pw')
        self.assertTrue('success' in response1)
        response2 = BeatMyGoalUser.create('user1', 'email2@gmail.com', 'pw')
        self.assertFalse('success' in response2)
        self.assertTrue('errors' in response2)
        self.assertTrue('username' in response2['errors'])
        self.assertFalse('email' in response2['errors'])
    
    def testCreateDuplicateEmail(self):
        """
        Tests that creating account with already existing email works
        """
        response1 = BeatMyGoalUser.create('user1', 'email1@gmail.com', 'pw')
        self.assertTrue('success' in response1)
        response2 = BeatMyGoalUser.create('user2', 'email1@gmail.com', 'pw')
        self.assertFalse('success' in response2)
        self.assertTrue('errors' in response2)
        self.assertFalse('username' in response2['errors'])
        self.assertTrue('email' in response2['errors'])
            
    def testCreateInvalidUsername(self):
        """
        Tests that creating account with invalid username
        """
        response = BeatMyGoalUser.create('##', 'email1@gmail.com', 'pw')
        self.assertFalse('success' in response)
        self.assertTrue('errors' in response)

    def testCreateInvalidEmail(self):
        """
        Tests that creating account with invalid email
        """
        response = BeatMyGoalUser.create('user1', 'email1', 'pw')
        self.assertFalse('success' in response)
        self.assertTrue('errors' in response)
            
    def testCreateInvalidPassword(self):
        """
        Tests that creating account with invalid password
        """
        response = BeatMyGoalUser.create('user1', 'email1@gmail.com', '##')
        self.assertFalse('success' in response)
        self.assertTrue('errors' in response)

    def testCreateEmptyUsername(self):
        """
        Tests that creating account with empty username
        """
        response = BeatMyGoalUser.create('', 'email1@gmail.com', 'pw')
        self.assertFalse('success' in response)
        self.assertTrue('errors' in response)

    def testCreateEmptyEmail(self):
        """
        Tests that creating account with empty email
        """
        response = BeatMyGoalUser.create('user1', '', 'pw')
        self.assertFalse('success' in response)
        self.assertTrue('errors' in response)

    def testCreateEmptyPassword(self):
        """
        Tests that creating account with empty email
        """
        response = BeatMyGoalUser.create('user1', 'email1@gmail.com', '')
        self.assertFalse('success' in response)
        self.assertTrue('errors' in response)

    def testLoginUser(self):
        """
        Tests login with registered username
        """
        BeatMyGoalUser.create('user1', 'email1@gmail.com', 'pw')
        response = BeatMyGoalUser.login('user1', 'pw')
        self.assertTrue('success' in response)
        self.assertFalse('errors' in response)

    def testLoginInvalidUser(self):
        """
        Tests login with unregistered username
        """
        response = BeatMyGoalUser.login('user1','pw')
        self.assertFalse('success' in response)
        self.assertTrue('errors' in response)

    def testLoginInvalidPassword(self):
        """
        Tests login with wrong password
        """
        BeatMyGoalUser.create('user1', 'email1@gmail.com', 'pw')
        response = BeatMyGoalUser.login('user1','pww')
        self.assertFalse('success' in response)
        self.assertTrue('errors' in response)


class User_View_Test(unittest.TestCase):
    def setUp(self):
        BeatMyGoalUser.objects.all().delete()
        Goal.objects.all().delete()
    

    def testGetUserMethods1(self):
        """
        test getUserById method in models
        """
        responce = BeatMyGoalUser.create('test_user_view','test_email_view','test_password_view')
        test_user = responce['user']
        test_user_userid = test_user.id
        test_user_username = test_user.username
        test_user_email = test_user.email
        user = BeatMyGoalUser.getUserById(test_user_userid)
        self.assertEqual(test_user_userid,user.id)
        self.assertEqual(test_user_username,user.username)
        self.assertEqual(test_user_email,user.email)

    
    def testGetUserMethods2(self):
        """
        test getUserByName method in models
        """
        responce = BeatMyGoalUser.create('test_user_view','test_email_view','test_password_view')
        test_user = responce['user']
        test_user_userid = test_user.id
        test_user_username = test_user.username
        test_user_email = test_user.email
        user = BeatMyGoalUser.getUserByName(test_user_username)
        self.assertEqual(test_user_userid,user.id)
        self.assertEqual(test_user_username,user.username)
        self.assertEqual(test_user_email,user.email)

    
    def testGetUserMethods3(self):
        """
        test getUserByName method in models
        """
        user = BeatMyGoalUser.getUserById(-99)
        self.assertEqual(-7,user)

    def testGetUserMethods4(self):
        """
        test getUserByName method in models
        """
        user = BeatMyGoalUser.getUserByName("")
        self.assertEqual(-2,user)

    def testDeleteUserMethod(self):
        """
        test delete method in models
        """
        responce = BeatMyGoalUser.create('test_user_view','test_email_view','test_password_view')
        test_user = responce['user']
        test_user_userid = test_user.id
        response = BeatMyGoalUser.delete(test_user_userid)
        self.assertEqual(response,1)
        self.assertEqual(BeatMyGoalUser.getUserById(test_user_userid),-7)

    def testDeleteUserMethod(self):
        """
        test delete method in models
        """
        response = BeatMyGoalUser.delete(-99)
        self.assertEqual(response,-7)

    def testEditGoal1(self):
        pass
    def testEditGoal2(self):
        pass
    def testEditGoal3(self):
        pass
    def testEditGoal4(self):
        pass
    def testEditGoal5(self):
        pass

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
    


