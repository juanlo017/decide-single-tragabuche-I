import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

class TraduccionesUITestCase(unittest.TestCase):
    
    def setUp(self):
        #indica el uso de chromium
        options = webdriver.ChromeOptions()
        options.headless = True
        self.driver = webdriver.Chrome(options=options)
        #abre la pagina
        self.driver.get("http://localhost:8000/authentication/register/")

    def test_traduccion_idioma_espanyol_selenium(self):
        
        selector_de_idioma = self.driver.find_element(By.ID,"id_language")

        #cambiamos al idioma español
        self.selector_idioma(selector_de_idioma,"es")

        #comprueba la traduccion al español
        expected_text_es = "Registro"
        element_es = self.driver.find_element(By.TAG_NAME, "h2")
        actual_text_es = element_es.text
        self.assertEqual(actual_text_es,expected_text_es)

    def selector_idioma(self, selector,language_id):
        #se usa select para usar el elemento select de la pagina
        select = Select(selector)
        #se escoge el idioma segun el id dado
        select.select_by_value(language_id)

    def tearDown(self):
        #se cierra chrome
        self.driver.quit()


