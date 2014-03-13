from core.models import Goal, BeatMyGoalUser
import unittest
from django.test import TestCase
from django.contrib.auth.models import User

class UserTest(unittest.TestCase):
	def setUp(self):
		User.objects.all().delete()
		Goal.objects.all().delete()
		BeatMyGoalUser.create('test_user','test_email','test_password')

	def testCreateUser1(self):
		pass
	def testCreateUser2(self):
		pass
	def testCreateUser3(self):		
		pass
	def testCreateUser4(self):
		pass
	def testCreateUser5(self):
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