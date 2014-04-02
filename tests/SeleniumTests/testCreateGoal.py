from django.test import LiveServerTestCase
from selenium import webdriver
from core.models import *
import time as time

class CreateGoalTestWithInvalidInput(LiveServerTestCase):
    def setUp(self):

        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(5)

        self.username = self.password = "kyle"
        self.email = "kyle@gmail.com"
        BeatMyGoalUser.create(self.username, self.email, self.password)

        
    def tearDown(self):
        self.driver.quit()
        time.sleep(1)


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


    def test_create_goal_test_with_invalid_input(self):
        """
        Try creating a goal with invalid inputs
        """
        driver = self.driver
        self.driver.get(self.live_server_url)
        self.login("kyle", "kyle")

        driver.find_element_by_link_text("Create Goal").click()
        driver.find_element_by_id("register-title").clear()
        driver.find_element_by_id("register-title").send_keys("Test With Invalid Input")
        driver.find_element_by_id("register-submit").click()
        time.sleep(1)

        self.assertTrue('Create' in driver.title, "Goal was created with invalid input")
    
    def test_create_timebased_goal(self):
        driver = self.driver
        self.driver.get(self.live_server_url)
        self.login("kyle", "kyle")

        driver.find_element_by_link_text("Create Goal").click()
        driver.find_element_by_id("register-title").clear()
        driver.find_element_by_id("register-title").send_keys("This is Test Case for Creating Value-based Goal")
        driver.find_element_by_id("register-description").clear()
        driver.find_element_by_id("register-description").send_keys("test Description")
        driver.find_element_by_id("register-prize").clear()
        driver.find_element_by_id("register-prize").send_keys("become software master")
        driver.find_element_by_id("register-end-value").clear()
        driver.find_element_by_id("register-end-value").send_keys("500")
        driver.find_element_by_id("register-value-unit").clear()
        driver.find_element_by_id("register-value-unit").send_keys("dollar")
        driver.find_element_by_id("deadline").click()
        driver.find_element_by_id("datepicker").click()
        driver.find_element_by_css_selector("span.ui-icon.ui-icon-circle-triangle-e").click()
        driver.find_element_by_link_text("16").click()
        driver.find_element_by_id("register-submit").click()
        
        self.assertTrue('This is Test Case for Creating Value-based Goal' in driver.title, "Goal was created with invalid input")
        time.sleep(1)

    def test_create_valuebased_goal(self):
        driver = self.driver
        self.driver.get(self.live_server_url)
        self.login("kyle", "kyle")
        
        driver.find_element_by_link_text("Create Goal").click()
        driver.find_element_by_id("register-title").clear()
        driver.find_element_by_id("register-title").send_keys("This is Test Case for Creating Value-based Goal")
        driver.find_element_by_id("register-description").clear()
        driver.find_element_by_id("register-description").send_keys("test description")
        driver.find_element_by_id("register-prize").clear()
        driver.find_element_by_id("register-prize").send_keys("become software master")
        driver.find_element_by_id("register-end-value").clear()
        driver.find_element_by_id("register-end-value").send_keys("500")
        driver.find_element_by_id("register-value-unit").clear()
        driver.find_element_by_id("register-value-unit").send_keys("dollar")
        driver.find_element_by_id("register-submit").click()
        
        self.assertTrue('This is Test Case for Creating Value-based Goal' in driver.title, "Goal was created with invalid input")
        time.sleep(1)