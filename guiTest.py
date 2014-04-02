import os
os.environ["DJANGO_SETTINGS_MODULE"] = "beatmygoal.settings"

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import unittest, re

from core.models import *
from core.constants import *
import time as time

# Put all GuiTests under this class
class GuiTests(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "http://localhost:8000/"
        self.verificationErrors = []
        self.accept_next_alert = True

        # Set up any objects you need here
        # ** Note! This works on your local db.sqlite, so be defensive
        # and delete any existing objects if it might cause a problem. **
        BeatMyGoalUser.objects.filter(username="arjun").delete()
        BeatMyGoalUser.create("arjun", "arjun@example.com", "arjun")
    
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
        driver.get(self.base_url)
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
    
    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException, e: return False
        return True
    
    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException, e: return False
        return True
    
    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True
    
    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
