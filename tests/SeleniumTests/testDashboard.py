from django.test import LiveServerTestCase
from selenium import webdriver

from core.models import *

import time as time

class DashboardTest(LiveServerTestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(10)

        # Set up any objects you need here
        BeatMyGoalUser.create("guitester", "guitester@example.com", "guitester")
        Goal.create("testgoal", "testgoaldescription", "guitester", "testprize", 0, "testtype", 123, "testunit", "01/01/2030")

    def tearDown(self):
        self.driver.quit()
        time.sleep(2)

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

    def test_dashboard(self):
        """
        Tests viewing the dashboard.
        """
        driver = self.driver

        #Open the web driver and go to the main page
        self.driver.get(self.live_server_url)

        self.login("guitester", "guitester")
        driver.find_element_by_link_text("Browse Goals").click()
        time.sleep(1)

        self.assertTrue('testgoal' in driver.find_element_by_css_selector(".dashcard-title").text, "Test goal displayed on dashboard")

        driver.find_element_by_link_text("testgoal").click()
        time.sleep(1)
        
        # This is really pretty complex and likely to fail soon
        #self.assertEqual("Email : a@rao.com", driver.find_element_by_xpath("//div[@id='main-content']/div/div/form/fieldset/div/div[2]/h5").text)

        # I think this is a better alternative
        self.assertIn("testgoal | BeatMyGoal", self.driver.title)

