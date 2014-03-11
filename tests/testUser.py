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
	def testCreateUser1(self):
	def testCreateUser1(self):		
	def testCreateUser1(self):
	def testCreateUser1(self):
	
	def testEditGoal(self):
	def testEditGoal(self):
	def testEditGoal(self):
	def testEditGoal(self):
	def testEditGoal(self):
	
	def testRemoveGoal(self):
	def testRemoveGoal(self):
	def testRemoveGoal(self):
	def testRemoveGoal(self):
	def testRemoveGoal(self):