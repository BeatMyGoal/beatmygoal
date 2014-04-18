from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from core.models import *

import time as time

class FavoriteTest(LiveServerTestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(10)

        # Set up any objects you need here
        BeatMyGoalUser.create("guitester", "guitester@example.com", "guitester")
        BeatMyGoalUser.create("creator", "creator@example.com", "creator")
        Goal.create("testgoal", "testgoaldescription", "creator", "testprize", 0, "testtype", "testendvalue", "testunit", "01/01/2030")

    

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



    def testJoinGoalButtonNotPresentWhenNotLoggedIn(self):
        """
        Test Join Goal button not present when not logged in
        """
        driver = self.driver
        self.driver.get(self.live_server_url)
        driver.find_element_by_link_text("Browse Goals").click()
        driver.find_element_by_link_text("testgoal").click()
        self.assertIn("testgoal | BeatMyGoal", self.driver.title)
        self.assertFalse("Join Goal" in driver.page_source, "Join Goal button is found")

    def testRegisterAndJoinButtonPresentWhenNotLoggedIn(self):
        """
        Test Register and join button is present when not logged in
        """
        driver = self.driver
        self.driver.get(self.live_server_url)
        driver.find_element_by_link_text("Browse Goals").click()
        driver.find_element_by_link_text("testgoal").click()
        self.assertIn("testgoal | BeatMyGoal", self.driver.title)
        self.assertTrue("Register and Join" in driver.page_source, "Register and Join button is not found")

    def testRegisterAndJoinButtonNotPresentWhenLoggedIn(self):
        """
        Test register and join button is not present when authenticated
        """
        driver = self.driver
        self.driver.get(self.live_server_url)
        self.login("guitester", "guitester")
        driver.find_element_by_link_text("Browse Goals").click()
        driver.find_element_by_link_text("testgoal").click()
        self.assertIn("testgoal | BeatMyGoal", self.driver.title)
        self.assertFalse("Register and Join" in driver.page_source, "Register and Join button is found")



    def testRegisterAndJoin(self):
        """
        Test register and join works
        """
        driver = self.driver
        self.driver.get(self.live_server_url)
        driver.find_element_by_link_text("Browse Goals").click()
        driver.find_element_by_link_text("testgoal").click()
        self.assertIn("testgoal | BeatMyGoal", self.driver.title)
        self.assertTrue("Register and Join" in driver.page_source, "Register and Join button is not found")
        driver.find_element_by_link_text("Register and Join").click()
        driver.find_element_by_id("register-username").clear()
        driver.find_element_by_id("register-username").send_keys("test123")
        driver.find_element_by_id("register-email").clear()
        driver.find_element_by_id("register-email").send_keys("test123@test123")
        driver.find_element_by_id("register-password").clear()
        driver.find_element_by_id("register-password").send_keys("test123")
        driver.find_element_by_id("register-submit").click()
        self.assertIn("testgoal | BeatMyGoal", self.driver.title)
        time.sleep(1)

    def tearDown(self):
        self.driver.quit()
        time.sleep(1)