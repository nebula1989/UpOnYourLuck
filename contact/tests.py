import time

# selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

from django.core.mail import send_mail
from django.test import TestCase
from contact.forms import ContactForm

# Create your tests here.
from uponyourluck import settings


class ContactFormModel(TestCase):
    def test_form_validation(self):
        form_data = {"email": "autotest@email.com", "name": "Tester Bot", "message": "This is a tester email"}
        form = ContactForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_send_email(self):
        name = "django-tester2@mail.com"
        email_subject = 'Test Subject'
        email_message = 'This is a test'
        self.assertTrue(
            bool(
                send_mail(
                    subject=email_subject, message=email_message, from_email=name,
                    recipient_list=(settings.CONTACT_EMAIL, settings.ADMIN_EMAILS)
                )
            )
        )


class SeleniumWebAutomation(TestCase):
    driver = webdriver.Firefox()
    #domain = settings.DOMAIN
    domain = 'http://www.uponyourluck.life/'

    def test_contact_form(self):
        """self.driver.get(self.domain + 'contact/')
        self.assertIn("Contact", self.driver.title)"""

        try:
            self.fill_in_contact_form('testing1@mail.com', 'George Clooney', 'Hi I am George')

        except NoSuchElementException:
            self.no_element_found()

    def test_duplicate_email(self):
        # this script will try to enter the same email 4 times
        for i in range(3):
            self.driver.get(self.domain + 'contact/')
            self.assertIn("Contact", self.driver.title)
            try:
                self.fill_in_contact_form('testing1@mail.com', 'George Clooney', 'Hi I am George')
                time.sleep(5)

            except NoSuchElementException:
                self.no_element_found()

    def fill_in_contact_form(self, email, name, message):
        email_field = self.driver.find_element(By.ID, 'id_email')
        email_field.send_keys(email)
        name_field = self.driver.find_element(By.ID, 'id_subject')
        name_field.send_keys(name)
        message_field = self.driver.find_element(By.ID, 'id_message')
        message_field.send_keys(message)
        time.sleep(10)
        submit_btn = self.driver.find_element(By.XPATH, "//input[@id='submit']")
        submit_btn.send_keys(Keys.RETURN)

    def no_element_found(self):
        print("Can't find elements.")
        self.driver.close()