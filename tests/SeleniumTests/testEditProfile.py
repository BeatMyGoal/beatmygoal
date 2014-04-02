from django.test import LiveServerTestCase
from selenium import webdriver

from core.models import *

import time as time

class EditUserTest(LiveServerTestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(10)

        # Set up any objects you need here
        BeatMyGoalUser.create("arjun", "arjun@example.com", "arjun")

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

    def test_edit_profile(self):
        """
        Tests editing the profile.
        """
        driver = self.driver

        #Open the web driver and go to the main page
        self.driver.get(self.live_server_url)

        self.login("arjun", "arjun")
        driver.find_element_by_link_text("arjun").click()
        time.sleep(1)
        driver.find_element_by_link_text("Edit User").click()
        time.sleep(1)
        driver.find_element_by_id("password").clear()
        driver.find_element_by_id("password").send_keys("arjun")
        driver.find_element_by_id("Confirm_button").click()
        time.sleep(1)
        
        self.assertTrue('Edit Profile' in driver.title, "Edit Profile page worked")

        driver.find_element_by_id("password").clear()
        driver.find_element_by_id("password").send_keys("arjun")
        driver.find_element_by_id("email").clear()
        driver.find_element_by_id("email").send_keys("a@rao.com")
        driver.find_element_by_id("save").click()
        time.sleep(1)
        
        # This is really pretty complex and likely to fail soon
        #self.assertEqual("Email : a@rao.com", driver.find_element_by_xpath("//div[@id='main-content']/div/div/form/fieldset/div/div[2]/h5").text)

        # I think this is a better alternative
        self.assertTrue('a@rao.com' in driver.find_element_by_css_selector("BODY").text, "Email was updated after editing")

