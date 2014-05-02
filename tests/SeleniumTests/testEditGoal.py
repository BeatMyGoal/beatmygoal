from django.test import LiveServerTestCase
from selenium import webdriver

from core.models import *

import time as time

class EditGoalTest(LiveServerTestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(10)

        # Set up any objects you need here
        BeatMyGoalUser.create("guitester", "guitester@example.com", "guitester")
        Goal.create("testgoal", "testgoaldescription", "guitester", "testprize", 0, "testtype", 20, "testunit", "01/01/2030")

    

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

    def testEditGoal(self):
        """
        Test editing a goal with valid inputs
        """
        driver = self.driver
        self.driver.get(self.live_server_url)
        self.login("guitester", "guitester")
        driver.find_element_by_link_text("Browse Goals").click()
        driver.find_element_by_link_text("testgoal").click()
        self.assertIn("testgoal | BeatMyGoal", self.driver.title)
        driver.find_element_by_link_text("Edit Goal").click()
        self.assertIn("Edit Goal | BeatMyGoal", self.driver.title)


        driver.find_element_by_id("title").clear()
        driver.find_element_by_id("title").send_keys("New Title")
        driver.find_element_by_id("description").clear()
        driver.find_element_by_id("description").send_keys("New Description")
        driver.find_element_by_id("ending_value").clear()
        driver.find_element_by_id("ending_value").send_keys("200")
        driver.find_element_by_id("unit").clear()
        driver.find_element_by_id("unit").send_keys("new unit")
        driver.find_element_by_link_text("Save").click()
        time.sleep(1)
        driver.find_element_by_css_selector("#reveal_save > label > #password").clear()
        driver.find_element_by_css_selector("#reveal_save > label > #password").send_keys("guitester")
        driver.find_element_by_id("Confirm_button").click()
        time.sleep(1)
        self.assertIn("New Title | BeatMyGoal", self.driver.title)

    def testEditGoalWithInvalidInput(self):
        """
        Test editing a goal with invalid inputs
        """
        driver = self.driver
        self.driver.get(self.live_server_url)
        self.login("guitester", "guitester")
        driver.find_element_by_link_text("Browse Goals").click()
        driver.find_element_by_link_text("testgoal").click()
        time.sleep(1)
        self.assertIn("testgoal | BeatMyGoal", self.driver.title)

        driver.find_element_by_link_text("Edit Goal").click()
        self.assertIn("Edit Goal | BeatMyGoal", self.driver.title)

        driver.find_element_by_id("title").clear()
        driver.find_element_by_id("title").send_keys("")
        driver.find_element_by_id("description").clear()
        driver.find_element_by_id("description").send_keys("New Description")
        driver.find_element_by_id("ending_value").clear()
        driver.find_element_by_id("ending_value").send_keys("200")
        driver.find_element_by_id("unit").clear()
        driver.find_element_by_id("unit").send_keys("new unit")

        self.assertIn("A Title Is Required", self.driver.find_element_by_id("title-error").text)


    def tearDown(self):
        self.driver.quit()
        time.sleep(1)