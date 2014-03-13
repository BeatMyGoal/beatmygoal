from core.models import Goal, BeatMyGoalUser
import unittest
from django.test import TestCase
from django.contrib.auth.models import User

class GoalTest(unittest.TestCase):
	def setUp(self):
		User.objects.all().delete()
		Goal.objects.all().delete()
		BeatMyGoalUser.create('test_user','test_email','test_password')
		

	#Test witih valid data
	def testCreateGoal1(self):
		response = Goal.create('test_title','test_description','test_user','test_prize',1,'test_goal_type')
		self.assertTrue('success' in response)
		g = Goal.objects.get(title='test_title')
		self.assertEqual('test_description', g.description)
		self.assertEqual('test_user',g.creator.username)
		self.assertEqual('test_prize', g.prize)
		self.assertEqual(1.0, g.private_setting)
		self.assertEqual('test_goal_type',g.goal_type)
		g.delete()


	#Test with valid data
	def testCreateGoal2(self):
		response = Goal.create('sample_title','sample_description','test_user','test_prize',2,'test_goal_type')
		self.assertTrue('success' in response)
		g = Goal.objects.get(title='sample_title')
		self.assertEqual('sample_description', g.description)
		self.assertEqual('test_user',g.creator.username)
		self.assertEqual('test_prize', g.prize)
		self.assertEqual(2, g.private_setting)
		self.assertEqual('test_goal_type',g.goal_type)
		g.delete()


	#Test with invalid title
	def testCreateGoal3(self):
		response = Goal.create('','sample_description','test_user','test_prize',2,'test_goal_type')
		self.assertFalse('success' in response)
		self.assertTrue('errors' in response)
		self.assertTrue('title' in response['errors'])
		self.assertFalse('description' in response['errors'])
		self.assertFalse('prize' in response['errors'])
		self.assertFalse('goal_type' in response['errors'])


	#Test with invalid title, description and prize
	def testCreateGoal4(self):
		response = Goal.create('','','test_user','',2,'test_goal_type')
		self.assertFalse('succes' in response)
		self.assertTrue('errors' in response)
		self.assertTrue('title' in response['errors'])
		self.assertTrue('description' in response['errors'])
		self.assertTrue('prize' in response['errors'])

	#Test with valid data, except user is invalid
	def testCreateGoal5(self):
		response = Goal.create('title','sample_description','invalid_user','test_prize',2,'test_goal_type')
		self.assertFalse('success' in response)
		self.assertTrue('errors' in response)
		self.assertTrue('user' in response['errors'])

	#Test editGoal with valid data
	def testEditGoal1(self):
		Goal.create('title','sample_description','test_user','test_prize',2,'test_goal_type')
		g = Goal.objects.get(id=1)
		edits = {'title':'newTitle','description':'newDescription'}
		response = Goal.edit(g,edits)
		g = Goal.objects.get(id=1)
		self.assertTrue('success' in response)
		self.assertFalse('errors' in response)
		self.assertEqual(g.title, 'newTitle')
		self.assertEqual(g.description, 'newDescription')

	#Test editGoal with invalid data
	def testEditGoal2(self):
		Goal.create('title','sample_description','test_user','test_prize',2,'test_goal_type')
		edits = {'title':'','description':''}
		g = Goal.objects.get(id=1)
		response = Goal.edit(g, edits)
		g = Goal.objects.get(id=1)
		self.assertFalse('success' in response)
		self.assertTrue('errors' in response)
		self.assertTrue('title' in response['errors'])
		self.assertTrue('description' in response['errors'])

	#Test editGoal with unmodified data
	def testEditGoal3(self):
		Goal.create('title','sample_description','test_user','test_prize',2,'test_goal_type')
		edits = {'title':'title','sample_description':''}
		g = Goal.objects.get(id=1)
		response = Goal.edit(g, edits)
		g = Goal.objects.get(id=1)
		self.assertTrue('success' in response)
		self.assertFalse('errors' in response)
		self.assertEqual('title', g.title)
		self.assertEqual('sample_description', g.description)

	#Test editGoal with no edits
	def testEditGoal4(self):
		Goal.create('title','sample_description','test_user','test_prize',2,'test_goal_type')
		edits = {}
		g = Goal.objects.get(id=1)
		response = Goal.edit(g, edits)
		self.assertTrue('success' in response)
		self.assertFalse('errors' in response)
		self.assertEqual('title', g.title)
		self.assertEqual('sample_description', g.description)

	


