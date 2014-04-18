from core.models import *
from core.constants import *
import unittest
from django.test import TestCase
from django.contrib.auth.models import User
from datetime import *

class LogTest(unittest.TestCase):
    def setUp(self):
        self.user = BeatMyGoalUser.create('test_user','test_email','test_password')['user']
        self.goal = Goal.create('sample_title','sample_description','test_user','test_prize',2,'test_goal_type', '500','dollars','4/23/2015')['goal']

    def testLogCreated(self):
        res = Goal.create('sample_title','sample_description','test_user','test_prize',2,'test_goal_type', '500','dollars','4/23/2015')
        goal = res['goal']
        self.assertTrue(goal.log)
        self.assertTrue(goal.log.goal is goal)

    def testLogEntryCreated(self):
        res = LogEntry.create(self.goal.log, "test_user", 20, "hello world")
        le = res['logEntry']
        self.assertTrue(self.goal.log.logentry_set.get(entry_amount=20))
        self.assertTrue(le.log is self.goal.log)

    def testLogEntryNonNumber(self):
        res = LogEntry.create(self.goal.log, "test_user", "badAmount", "hello world")
        self.assertTrue(CODE_BAD_AMOUNT in res['errors'])

    def testGetLogEntriesByUsers(self):
        le_res = LogEntry.create(self.goal.log, "test_user", 20, "hello world")
        le = le_res['logEntry']
        res = le.log.parseEntriesByUser()
        self.assertTrue(20 in res['users'][0][1])
