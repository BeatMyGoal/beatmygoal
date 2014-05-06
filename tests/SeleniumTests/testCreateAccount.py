from django.test import LiveServerTestCase
from selenium import webdriver

from core.models import *

import time as time

class EditUserTest(LiveServerTestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(10)

        # Set up any objects you need here

    def tearDown(self):
        self.driver.quit()
        time.sleep(2)

    def test_create_account(self):
        """
        Tests creating an account with valid credentials.
        """
        driver = self.driver

        #Open the web driver and go to the main page
        self.driver.get(self.live_server_url)

        driver.find_element_by_id("register-username").clear()
        driver.find_element_by_id("register-username").send_keys("arjun")
        driver.find_element_by_id("register-email").clear()
        driver.find_element_by_id("register-email").send_keys("arjun@aol.com")
        driver.find_element_by_id("register-password").clear()
        driver.find_element_by_id("register-password").send_keys("arjun")
        driver.find_element_by_id("register-confirm-password").clear()
        driver.find_element_by_id("register-confirm-password").send_keys("arjun")
        driver.find_element_by_id("register-submit").click()

        time.sleep(2)
        
        self.assertTrue('arjun' in driver.title, "Redirect to profile worked")

    def test_create_account_invalid(self):
        """
        Tests creating an account with invalid credentials.
        """
        driver = self.driver

        #Open the web driver and go to the main page
        self.driver.get(self.live_server_url)

        driver.find_element_by_id("register-username").clear()
        driver.find_element_by_id("register-username").send_keys("arjun")
        driver.find_element_by_id("register-email").clear()
        driver.find_element_by_id("register-email").send_keys("bademail")

        driver.find_element_by_id("register-submit").click()

        time.sleep(2)
         
        self.assertTrue('Home' in driver.title, "Registration without password went thru")

        driver.find_element_by_id("register-password").clear()
        driver.find_element_by_id("register-password").send_keys("password")

        driver.find_element_by_id("register-submit").click()
        time.sleep(2)

        self.assertTrue('Home' in driver.title, "Registration with bad email went thru")



