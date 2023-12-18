from django.test import TestCase
from base.tests import BaseTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from voting.models import Voting, Question, QuestionOption
from django.contrib.auth.models import User

class VotingSeleniumTestCase(StaticLiveServerTestCase):

    def setUp(self):
        #Crea un usuario admin y otro no admin
        self.base = BaseTestCase()
        self.base.setUp()
        admin = User.objects.get(username='admin')
        admin.is_superuser = True
        admin.save()
	
        #Opciones de Chrome
        options = webdriver.ChromeOptions()
        options.headless = True
        self.driver = webdriver.Chrome(options=options)

        super().setUp()

    def tearDown(self):           
        super().tearDown()
        self.driver.quit()

        self.base.tearDown()

    def test_create_yes_no_question(self):             
        self.driver.get(f'{self.live_server_url}/admin/')
        self.driver.find_element(By.ID,'id_username').send_keys("admin")
        self.driver.find_element(By.ID,'id_password').send_keys("qwerty",Keys.ENTER) 

        #Crear pregunta Yes/No
        self.driver.get(f'{self.live_server_url}/admin/voting/question/add/')
        self.driver.find_element(By.ID,'id_desc').send_keys("Prueba de pregunta Yes/No")
        self.driver.find_element(By.ID,'id_yes_no').click()

        self.driver.find_element(By.NAME,'_save').click()

        #Mirar si se ha creado
        self.assertTrue(self.driver.current_url.endswith('/admin/voting/question/'))
        self.assertIn("Prueba de pregunta Yes/No", self.driver.page_source)

        self.driver.find_element(By.LINK_TEXT,'Prueba de pregunta Yes/No').click()

        question_desc = self.driver.find_element(By.ID,'id_desc').get_attribute('value')
        self.assertEqual(question_desc, "Prueba de pregunta Yes/No")
        option_yes = self.driver.find_element(By.ID,'id_options-0-option').get_attribute('value')
        self.assertEqual(option_yes, "Yes")
        option_no = self.driver.find_element(By.ID,'id_options-1-option').get_attribute('value')
        self.assertEqual(option_no, "No")
        

    
