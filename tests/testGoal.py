from core.models import Goal, BeatMyGoalUser
import unittest
from django.test import TestCase
from django.contrib.auth.models import User

class GoalTest(unittest.TestCase):
	def setUp(self):
		User.objects.all().delete()
		Goal.objects.all().delete()
		BeatMyGoalUser.create('test_user','test_email','test_password')
		


	def testCreateGoal1(self):
		

		self.assertEqual(1, Goal.create('test_title','test_description','test_user','test_prize',1,'test_goal_type'))
		g = Goal.objects.get(title='test_title')
		self.assertEqual('test_description', g.description)
		self.assertEqual('test_user',g.creator.username)
		self.assertEqual('test_prize', g.prize)
		self.assertEqual(1.0, g.private_setting)
		self.assertEqual('test_goal_type',g.goal_type)
		g.delete()


	def testCreateGoal2(self):
		BeatMyGoalUser.create('test_user2','test_email','test_password')
		u = BeatMyGoalUser.getUserByName('test_user2')
		self.assertEqual(1, Goal.create('myGoal','myDescription','test_user2','myPrize',0,'myGoalType'))
		g = Goal.objects.get(description='myDescription')
		self.assertEqual('myGoal',g.title)
		self.assertEqual('myDescription',g.description)
		self.assertEqual('test_user2',g.creator.username)
		self.assertEqual(0,g.private_setting)
		self.assertEqual('myGoalType',g.goal_type)
		g.delete()

	def testCreateGoal3(self):
		self.assertEqual(-3, Goal.create('a'*51,'aa','aa','aa',1,'aa'))

	def testCreateGoal4(self):
		self.assertEqual(-4, Goal.create('a'*20,'a'*131,'aa','aa',1,'aa'))

	def testCreateGoal5(self):
		self.assertEqual(-4, Goal.create('a'*11, None ,'aa','aa',1,'aa'))

	def testCreateGoal6(self):
		self.assertEqual(-6, Goal.create('a','a','a','a'*51, 0,'a'))

	def testCreateGoal7(self):
		self.assertEqual(-2, Goal.create('wfwef','wefwefwef','non_existing_user','wefwef',1,'sometype'))

	def testRemoveGoal(self):
		Goal.create('test_title','test_description','test_user','test_prize',1,'test_goal_type')
		g = Goal.objects.get(title='test_title')
		self.assertEqual(1, Goal.remove(g.id,g.creator))
		a = Goal.objects.filter(id = g.id)
		self.assertEqual(0, len(a))
		g.delete()

	def testRemoveGoal2(self):
		BeatMyGoalUser.create('test_user4','test_email','test_password')
		BeatMyGoalUser.create('test_user5','test_email','test_password')
		Goal.create('test_title4','test_description','test_user4','test_prize',1,'test_goal_type')
		Goal.create('test_title5','test_description','test_user5','test_prize',1,'test_goal_type')
		g1 = Goal.objects.get(title='test_title4')
		g2 = Goal.objects.get(title='test_title5')
		self.assertEqual(-8, Goal.remove(g1.id, g2.creator))

	def testRemoveGoal3(self):
		u = BeatMyGoalUser.getUserByName('test_user')
		self.assertEqual(-7, Goal.remove(-1,u))

	def testRemoveGoal4(self):
		u = BeatMyGoalUser.getUserByName('test_user')
		self.assertEqual(-7, Goal.remove(3,u))

	def testEditGoal(self):
		BeatMyGoalUser.create('test_user4','test_email','test_password')
		Goal.create('test_title4','test_description','test_user4','test_prize',1,'test_goal_type')
		g = Goal.objects.get(title='test_title4')
		edits = {"title":"newTitle","description":"newDescription","private_setting":10}
		self.assertEqual(1, Goal.edit(g.id, g.creator,edits))
		g = Goal.objects.get(id=g.id)
		self.assertEqual("newTitle", g.title)
		self.assertEqual("newDescription",g.description)
		self.assertEqual(10,g.private_setting)

	def testEditGoal2(self):
		BeatMyGoalUser.create('test_user4','test_email','test_password')
		Goal.create('test_title4','test_description','test_user4','test_prize',1,'test_goal_type')
		g = Goal.objects.get(title='test_title4')
		self.assertEqual(-7, Goal.edit(23,g.creator,{}))

	def testEditGoal3(self):
		BeatMyGoalUser.create('test_user4','test_email','test_password')
		Goal.create('test_title4','test_description','test_user4','test_prize',1,'test_goal_type')
		g = Goal.objects.get(title='test_title4')
		self.assertEqual(1, Goal.edit(g.id, g.creator,{}))
		g = Goal.objects.get(id=g.id)
		self.assertEqual("test_title4", g.title)
		self.assertEqual("test_description",g.description)
		self.assertEqual(1,g.private_setting)

	def testEditGoal3(self):
		BeatMyGoalUser.create('test_user4','test_email','test_password')
		Goal.create('test_title4','test_description','test_user4','test_prize',1,'test_goal_type')
		g = Goal.objects.get(title='test_title4')
		self.assertEqual(-9, Goal.edit(g.id, g.creator,{"title":23904823094,"description":242424,"private_setting":"stringvalue"}))
