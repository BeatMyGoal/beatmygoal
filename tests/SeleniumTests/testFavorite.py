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
        Goal.create("testgoal", "testgoaldescription", "creator", "testprize", 0, "testtype", 230, "testunit", "01/01/2030")

    

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

    def testFavoriteButtonNotPresentWhenNotJoined(self):
        """
        Test editing a goal with valid inputs
        """
        driver = self.driver
        self.driver.get(self.live_server_url)
        self.login("guitester", "guitester")
        driver.find_element_by_link_text("Browse Goals").click()
        driver.find_element_by_link_text("testgoal").click()
        self.assertIn("testgoal | BeatMyGoal", self.driver.title)
        self.assertFalse("Add to Favorite" in driver.page_source, "Favorite button is found")

    def testFavoriteButtonPresentWhenJoined(self):
        """
        Test editing a goal with valid inputs
        """
        driver = self.driver
        self.driver.get(self.live_server_url)
        self.login("guitester", "guitester")
        driver.find_element_by_link_text("Browse Goals").click()
        driver.find_element_by_link_text("testgoal").click()
        self.assertIn("testgoal | BeatMyGoal", self.driver.title)
        driver.find_element_by_link_text("Join Goal").click()
        self.assertTrue("Add to Favorites" in driver.page_source, "Favorite button is not found")

    def testFavoriteGoalPresentInUserProfile(self):
        driver = self.driver
        self.driver.get(self.live_server_url)
        self.login("guitester", "guitester")
        driver.find_element_by_link_text("Browse Goals").click()
        driver.find_element_by_link_text("testgoal").click()
        self.assertIn("testgoal | BeatMyGoal", self.driver.title)
        driver.find_element_by_link_text("Join Goal").click()
        driver.find_element_by_link_text("Add to Favorites").click()
        driver.find_element_by_link_text("My Profile").click()


    def tearDown(self):
        self.driver.quit()
        time.sleep(1)