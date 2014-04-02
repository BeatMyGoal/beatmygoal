from django.test import LiveServerTestCase
from selenium import webdriver
import time

class MainPageTest(LiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(10)

        #Open the web browser and go to the main page
        self.browser.get(self.live_server_url)

    def tearDown(self):
        self.browser.quit()
        time.sleep(2)

    def test_title_of_the_main_page(self):
        """
        Test the title of the main page
        """
        self.assertIn("Home | BeatMyGoal", self.browser.title)

    def test_bmg_log_exists(self):
        """
        Test the Logo on the homepage
        """
        logo = self.browser.find_elements_by_class_name("fa.fa-trophy")
        self.assertTrue(logo != None)

    def test_top_bar_exists(self):
        """
        Test that topbar is loading
        """
        top_bar = self.browser.find_elements_by_class_name("top-bar")
        self.assertTrue(top_bar != None)

    def test_login_form_exists(self):
        """
        Test the login form exists
        """
        login_form = self.browser.find_elements_by_id("login-form")
        self.assertTrue(login_form != None)

    def test_register_forms_exist(self):
        """
        Test the registration form exists
        """
        register_username_field = self.browser.find_elements_by_id("register-username")
        register_password_field = self.browser.find_elements_by_id("register-password")
        register_email_field = self.browser.find_elements_by_id("register-password")
        self.assertTrue(register_username_field != None)
        self.assertTrue(register_password_field != None)
        self.assertTrue(register_email_field != None)
