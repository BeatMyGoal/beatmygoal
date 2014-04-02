from django.test import LiveServerTestCase
from selenium import webdriver

from core.models import *

import time as time

class EditUserTest(LiveServerTestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(10)

        # Set up any objects you need here
        self.username = self.password = "jay"
        self.email = "jay@example.com"
        BeatMyGoalUser.create(self.username, self.email, self.password)        

    def tearDown(self):
        self.driver.quit()
        time.sleep(2)

    def test_login(self):
        """
        Test logging in with valid credentials.
        """
        driver = self.driver
        self.driver.get(self.live_server_url)
        driver.find_element_by_id("topbar-login").click()
        driver.find_element_by_id("username").clear()
        driver.find_element_by_id("username").send_keys(self.username)
        driver.find_element_by_id("password").clear()
        driver.find_element_by_id("password").send_keys(self.password)
        driver.find_element_by_id("login").click()
        time.sleep(1)
        self.assertTrue('Dashboard' in driver.title, "Redirected to dashboard after login")

    def test_login_invalid(self):
        """
        Test logging in with invalid credentials.
        """
        driver = self.driver
        self.driver.get(self.live_server_url)
        orig = driver.title
        driver.find_element_by_id("topbar-login").click()
        driver.find_element_by_id("username").clear()
        driver.find_element_by_id("username").send_keys("fooply")
        driver.find_element_by_id("password").clear()
        driver.find_element_by_id("password").send_keys("fooply")
        driver.find_element_by_id("login").click()
        time.sleep(1)
        self.assertEqual(orig, driver.title, "Incorrectly changed pages after bad login")

