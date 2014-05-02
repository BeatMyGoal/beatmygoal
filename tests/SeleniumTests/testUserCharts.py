from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from core.models import *

import time as time

class ChartsTest(LiveServerTestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(10)

        # Set up any objects you need here
        BeatMyGoalUser.create("guitester", "guitester@example.com", "guitester")
        BeatMyGoalUser.create("creator", "creator@example.com", "creator")
        res1 = Goal.create("testgoal1", "testgoaldescription", "creator", "testprize", 40, "testtype", 200, "testunit", "01/01/2030")
        res2 = Goal.create("testgoal2", "testgoaldescription", "creator", "testprize", 40, "testtype", 200, "testunit", "01/01/2030")
        res3 = Goal.create("testgoal3", "testgoaldescription", "creator", "testprize", 40, "testtype", 200, "testunit", "01/01/2030")
        self.goal1 = res1['goal']
        self.goal2 = res2['goal']
        self.goal3 = res3['goal']
        LogEntry.create(self.goal1.log, "guitester", 20, "hello world")
        LogEntry.create(self.goal1.log, "guitester", 20, "hello world")
        LogEntry.create(self.goal1.log, "guitester", 20, "hello world")
        LogEntry.create(self.goal2.log, "guitester", 20, "hello world")
        LogEntry.create(self.goal3.log, "guitester", 20, "hello world")

    def login(self, username, password):
        """
        Logins a user using the GUI interface.
        """
        driver = self.driver
        driver.find_element_by_id("topbar-login").click()
        driver.find_element_by_id("username").clear()
        driver.find_element_by_id("username").send_keys(username)
        driver.find_element_by_id("password").clear()
        driver.find_element_by_id("password").send_keys(password)
        driver.find_element_by_id("login").click()
        time.sleep(1)

    def testLogProgressOverLastTwoWeeksExist(self):
        """
        Test Log Progress over last 2 weeks exist as a chart
        """
        driver = self.driver
        self.driver.get(self.live_server_url)
        self.login("guitester", "guitester")
        driver.find_element_by_link_text("My Profile").click()
        self.assertIn("guitester | BeatMyGoal", self.driver.title)
        self.assertTrue("Log progress over last 2 weeks" in driver.page_source, "Log progress over last 2 weeks chart not shown")

    def testNumberofLogsperGoalExist(self):
        """
        Test Number of logs per goal chart exist in user profile
        """
        driver = self.driver
        self.driver.get(self.live_server_url)
        self.login("guitester", "guitester")
        driver.find_element_by_link_text("My Profile").click()
        self.assertIn("guitester | BeatMyGoal", self.driver.title)
        self.assertTrue("Number of logs per goal" in driver.page_source, "Number of logs per goal not shown")

    def tearDown(self):
        self.driver.quit()
        time.sleep(1)