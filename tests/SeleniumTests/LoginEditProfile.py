from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import unittest, time, re

class LoginAndEditProfileFromIndex(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "http://localhost:8000/"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_login_and_edit_profile_from_index(self):
        driver = self.driver
        driver.get(self.base_url + "/")
        driver.find_element_by_id("username").clear()
        driver.find_element_by_id("username").send_keys("arjun")
        driver.find_element_by_id("password").clear()
        driver.find_element_by_id("password").send_keys("arjun")
        driver.find_element_by_id("login").click()
        driver.find_element_by_link_text("arjun").click()
        driver.find_element_by_link_text("Edit User").click()
        driver.find_element_by_id("password").clear()
        driver.find_element_by_id("password").send_keys("arjun")
        driver.find_element_by_id("Confirm_button").click()
        driver.find_element_by_id("password").clear()
        driver.find_element_by_id("password").send_keys("arjun")
        driver.find_element_by_id("email").clear()
        driver.find_element_by_id("email").send_keys("a@rao.com")
        driver.find_element_by_id("save").click()
        self.assertEqual("Email : a@rao.com", driver.find_element_by_xpath("//div[@id='main-content']/div/div/form/fieldset/div/div[2]/h5").text)
    
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
