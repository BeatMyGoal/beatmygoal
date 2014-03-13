from core.models import Goal, BeatMyGoalUser
import unittest
from django.test import TestCase
from django.contrib.auth.models import User


class UserTest(unittest.TestCase):
    def setUp(self):
        BeatMyGoalUser.objects.all().delete()
        Goal.objects.all().delete()
    
    def testCreateUser(self):
        "Tests that creating new user works"
        response = BeatMyGoalUser.create('user1', 'email1@gmail.com', 'pw')
        self.assertTrue('success' in response)
        userid = BeatMyGoalUser.objects.get(username = 'user1')
        self.assertEqual('email1@gmail.com', userid.email)
        self.assertEqual('pw', userid.password)

    def testCreateDuplicateUser(self):
        "Tests that creating account with already existing username works"
        response1 = BeatMyGoalUser.create('user1', 'email1@gmail.com', 'pw')
        self.assertTrue('success' in response1)
        response2 = BeatMyGoalUser.create('user1', 'email2@gmail.com', 'pw')
        self.assertFalse('success' in response2)
        self.assertTrue('errors' in response2)
        self.assertTrue('username' in response2['errors'])
        self.assertFalse('email' in response2['errors'])
    
    def testCreateDuplicateEmail(self):
        "Tests that creating account with already existing email works"
        response1 = BeatMyGoalUser.create('user1', 'email1@gmail.com', 'pw')
        self.assertTrue('success' in response1)
        response2 = BeatMyGoalUser.create('user2', 'email1@gmail.com', 'pw')
        self.assertFalse('success' in response2)
        self.assertTrue('errors' in response2)
        self.assertFalse('username' in response2['errors'])
        self.assertTrue('email' in response2['errors'])
            
    def testCreateInvalidUsername(self):
        "Tests that creating account with invalid username"
        response = BeatMyGoalUser.create('##', 'email1@gmail.com', 'pw')
        self.assertFalse('success' in response)
        self.assertTrue('errors' in response)

    def testCreateInvalidEmail(self):
        "Tests that creating account with invalid email"
        response = BeatMyGoalUser.create('user1', 'email1', 'pw')
        self.assertFalse('success' in response)
        self.assertTrue('errors' in response)
            
    def testCreateInvalidPassword(self):
        "Tests that creating account with invalid password"
        response = BeatMyGoalUser.create('user1', 'email1@gmail.com', '##')
        self.assertFalse('success' in response)
        self.assertTrue('errors' in response)

    def testCreateEmptyUsername(self):
        "Tests that creating account with empty username"
        response = BeatMyGoalUser.create('', 'email1@gmail.com', 'pw')
        self.assertFalse('success' in response)
        self.assertTrue('errors' in response)

    def testCreateEmptyEmail(self):
        "Tests that creating account with empty email"
        response = BeatMyGoalUser.create('user1', '', 'pw')
        self.assertFalse('success' in response)
        self.assertTrue('errors' in response)

    def testCreateEmptyPassword(self):
        "Tests that creating account with empty email"
        response = BeatMyGoalUser.create('user1', 'email1@gmail.com', '')
        self.assertFalse('success' in response)
        self.assertTrue('errors' in response)

    def testLoginUser(self):
        "Tests login with registered username"
        BeatMyGoalUser.create('user1', 'email1@gmail.com', 'pw')
        response = BeatMyGoalUser.login('user1', 'pw')
        self.assertTrue('success' in response)
        self.assertFalse('errors' in response)

    def testLoginInvalidUser(self):
        "Tests login with unregistered username"
        response = BeatMyGoalUser.login('user1','pw')
        self.assertFalse('success' in response)
        self.assertTrue('errors' in response)

    def testLoginInvalidPassword(self):
        "Tests login with wrong password"
        BeatMyGoalUser.create('user1', 'email1@gmail.com', 'pw')
        response = BeatMyGoalUser.login('user1','pww')
        self.assertFalse('success' in response)
        self.assertTrue('errors' in response)

	def testViewUser1(self):
		pass
	def testViewUser1(self):
		pass
	def testViewUser1(self):		
		pass
	def testViewUser1(self):
		pass
	def testViewUser1(self):
		pass
	
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
	
	def testRemoveGoal1(self):
		pass
	def testRemoveGoal2(self):
		pass
	def testRemoveGoal3(self):
		pass
	def testRemoveGoal4(self):
		pass
	def testRemoveGoal5(self):
		pass







