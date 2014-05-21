from django.test import LiveServerTestCase
from selenium import webdriver

from core.models import *

import time as time
import os
import sys
import httplib
import base64
import json
import new
import unittest
import sauceclient
from selenium import webdriver
from sauceclient import SauceClient

# it's best to remove the hardcoded defaults and always get these values
# from environment variables
USERNAME = os.environ.get('SAUCE_USERNAME', "kknd113")
ACCESS_KEY = os.environ.get('SAUCE_ACCESS_KEY', "fcdcdfc4-bf41-46b1-85b1-6feafaad3610")
sauce = SauceClient(USERNAME, ACCESS_KEY)

browsers = [{"platform": "Mac OS X 10.9",
             "browserName": "chrome",
             "version": ""},
            {"platform": "Windows 8.1",
             "browserName": "internet explorer",
             "version": "11"}]


def on_platforms(platforms):
    def decorator(base_class):
        module = sys.modules[base_class.__module__].__dict__
        for i, platform in enumerate(platforms):
            d = dict(base_class.__dict__)
            d['desired_capabilities'] = platform
            name = "%s_%s" % (base_class.__name__, i + 1)
            module[name] = new.classobj(name, (base_class,), d)
    return decorator



@on_platforms(browsers)
class EditUserTest(LiveServerTestCase):
    def setUp(self):
        self.desired_capabilities['name'] = self.id()

        sauce_url = "http://%s:%s@ondemand.saucelabs.com:80/wd/hub"
        self.driver = webdriver.Remote(
            desired_capabilities=self.desired_capabilities,
            command_executor=sauce_url % (USERNAME, ACCESS_KEY)
        )
        self.driver.implicitly_wait(30)
        # Set up any objects you need here

    def tearDown(self):
      print("Link to your job: https://saucelabs.com/jobs/%s" % self.driver.session_id)
      try:
          if sys.exc_info() == (None, None, None):
              sauce.jobs.update_job(self.driver.session_id, passed=True)
          else:
              sauce.jobs.update_job(self.driver.session_id, passed=False)
      finally:
          self.driver.quit()

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
