from core.models import *
from core.constants import *
import unittest
from django.test import TestCase
from django.contrib.auth.models import User

class GoalTest(unittest.TestCase):
    def setUp(self):
        BeatMyGoalUser.create('test_user','test_email','test_password')

    def tearDown(self):
        User.objects.all().delete()
        Goal.objects.all().delete()

    def testCreateGoalWithValidData1(self):
        """
        Test witih valid data
        """
        response = Goal.create('test_title','test_description','test_user','test_prize',1,'test_goal_type')
        self.assertTrue(not response['errors'])
        g = Goal.objects.get(title='test_title')
        self.assertEqual('test_description', g.description)
        self.assertEqual('test_user',g.creator.username)
        self.assertEqual('test_prize', g.prize)
        self.assertEqual(1.0, g.private_setting)
        self.assertEqual('test_goal_type',g.goal_type)
        g.delete()



    def testCreateGoalWithValidData2(self):
        """
        Test with valid data
        """
        response = Goal.create('sample_title','sample_description','test_user','test_prize',2,'test_goal_type')
        self.assertTrue(not response['errors'])
        g = Goal.objects.get(title='sample_title')
        self.assertEqual('sample_description', g.description)
        self.assertEqual('test_user',g.creator.username)
        self.assertEqual('test_prize', g.prize)
        self.assertEqual(2, g.private_setting)
        self.assertEqual('test_goal_type',g.goal_type)
        g.delete()



    def testCreateGoalWithInvalidData(self):
        """
        Test with invalid title
        """
        response = Goal.create('','sample_description','test_user','test_prize',2,'test_goal_type')
        self.assertFalse(not response['errors'])
        self.assertTrue(response['errors'])
        self.assertTrue(CODE_BAD_TITLE in response['errors'])
        self.assertFalse(CODE_BAD_DESCRIPTION in response['errors'])
        self.assertFalse(CODE_BAD_PRIZE in response['errors'])
        self.assertFalse(CODE_BAD_TYPE in response['errors'])



    def testCreateGoalWithInvalidTitle(self):
        """
        Test with invalid title, description and prize
        """
        response = Goal.create('','','test_user','',2,'test_goal_type')
        self.assertFalse(not response['errors'])
        self.assertTrue(response['errors'])
        self.assertTrue(CODE_BAD_TITLE in response['errors'])
        self.assertTrue(CODE_BAD_DESCRIPTION in response['errors'])
        self.assertTrue(CODE_BAD_PRIZE in response['errors'])




    def testEditGoalWithValidData1(self):
        """
        Test editGoal with valid data
        """
        Goal.create('title','sample_description','test_user','test_prize',2,'test_goal_type')
        g = Goal.objects.get(id=1)
        edits = {'title':'newTitle','description':'newDescription'}
        response = Goal.edit(g,edits)
        g = Goal.objects.get(id=1)
        self.assertTrue(not response['errors'])
        self.assertFalse(response['errors'])
        self.assertEqual(g.title, 'newTitle')
        self.assertEqual(g.description, 'newDescription')



    def testEditGoalWithValidData2(self):
        """
        Test editGoal with invalid data
        """
        Goal.create('title','sample_description','test_user','test_prize',2,'test_goal_type')
        edits = {'title':'','description':''}
        g = Goal.objects.get(id=1)
        response = Goal.edit(g, edits)
        g = Goal.objects.get(id=1)
        self.assertFalse(not response['errors'])
        self.assertTrue(response['errors'])
        self.assertTrue(CODE_BAD_TITLE in response['errors'])
        self.assertTrue(CODE_BAD_DESCRIPTION in response['errors'])


    def testEditGoalWithUnmodifiedData(self):
        """
        Test editGoal with unmodified data
        """
        Goal.create('title','sample_description','test_user','test_prize',2,'test_goal_type')
        edits = {'title':'title','sample_description':''}
        g = Goal.objects.get(id=1)
        response = Goal.edit(g, edits)
        g = Goal.objects.get(id=1)
        self.assertTrue(not response['errors'])
        self.assertFalse(response['errors'])
        self.assertEqual('title', g.title)
        self.assertEqual('sample_description', g.description)


    def testEditGoalWithNoEdits(self):
        """
        Test editGoal with no edits
        """
        Goal.create('title','sample_description','test_user','test_prize',2,'test_goal_type')
        edits = {}
        g = Goal.objects.get(id=1)
        response = Goal.edit(g, edits)
        self.assertTrue(not response['errors'])
        self.assertFalse(response['errors'])
        self.assertEqual('title', g.title)
        self.assertEqual('sample_description', g.description)


    def testRemoveGoalWithValidData(self):
        """
        Delete goal with valid data
        """
        Goal.create('title','sample_description','test_user','test_prize',2,'test_goal_type')
        g = Goal.objects.get(id=1)
        response = Goal.remove(g.id, g.creator.username)
        self.assertEqual(len(response['errors']), 0)
        lst = Goal.objects.filter(id=1)
        self.assertFalse(lst)


    def testRemoveGoalWithInvalidData(self):
        """
        Delete goal with invalid user
        """
        Goal.create('title','sample_description','test_user','test_prize',2,'test_goal_type')
        g = Goal.objects.get(id=1)
        response = Goal.remove(g.id, 'eh')
        self.assertTrue(CODE_GOAL_DNE in response['errors'])


    def testRemoveGoalWithInvalidUser(self):
        """
        Delete goal with invalid user
        """
        Goal.create('title','sample_description','test_user','test_prize',2,'test_goal_type')
        g = Goal.objects.get(id=1)
        response = Goal.remove(g.id, 'eh')
        self.assertTrue(CODE_GOAL_DNE in response['errors'])

    def testGoalCreatedWithLog(self):
        """
        Goal created with a log to create log entries
        """
        Goal.create('title','sample_description','test_user','test_prize',2,'test_goal_type')
        g = Goal.objects.get(id=1)
        self.assertTrue(g.log is not None)

    def testCreateLogEntry(self):
        """
        Create a log entry for a goal
        """
        Goal.create('title','sample_description','test_user','test_prize',2,'test_goal_type')
        g = Goal.objects.get(id=1)
        res = LogEntry.create(g.log, 'test_user', 100, 'test_comment')
        le = g.log.logentry_set.get(comment='test_comment')
        self.assertTrue(g.log.logentry_set.all())
        self.assertEqual(res['logEntry'], le)
        self.assertEqual(le.participant.username, 'test_user')
        self.assertEqual(le.entry_amount, 100)
        self.assertEqual(le.comment, 'test_comment')
