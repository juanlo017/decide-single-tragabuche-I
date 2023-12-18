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


    def test_traduccion_idioma_ingles_selenium(self):
        
        selector_de_idioma = self.driver.find_element(By.ID,"id_language")

        #cambiamos al idioma ingles
        self.selector_idioma(selector_de_idioma,"en")

        #comprueba la traduccion al ingles
        expected_text_en = "Registration"
        element_en = self.driver.find_element(By.TAG_NAME, "h2")
        actual_text_en = element_en.text
        self.assertEqual(actual_text_en,expected_text_en)

    def test_traduccion_idioma_frances_selenium(self):
        
        selector_de_idioma = self.driver.find_element(By.ID,"id_language")

        #cambiamos al idioma frances
        self.selector_idioma(selector_de_idioma,"fr")

        #comprueba la traduccion al frances
        expected_text_fr = "Enregistrer"
        element_fr = self.driver.find_element(By.TAG_NAME, "h2")
        actual_text_fr = element_fr.text
        self.assertEqual(actual_text_fr,expected_text_fr)


    def test_traduccion_idioma_esperanto_selenium(self):
        
        selector_de_idioma = self.driver.find_element(By.ID,"id_language")

        #cambiamos al idioma esperanto
        self.selector_idioma(selector_de_idioma,"eo")

        #comprueba la traduccion al esperanto
        expected_text_eo = "Rekordo"
        element_eo = self.driver.find_element(By.TAG_NAME, "h2")
        actual_text_eo = element_eo.text
        self.assertEqual(actual_text_eo,expected_text_eo)

    def test_traduccion_idioma_escoces_selenium(self):
        
        selector_de_idioma = self.driver.find_element(By.ID,"id_language")

        #cambiamos al idioma escoces
        self.selector_idioma(selector_de_idioma,"gd")

        #comprueba la traduccion al escoces
        expected_text_gd = "Clàr"
        element_gd = self.driver.find_element(By.TAG_NAME, "h2")
        actual_text_gd = element_gd.text
        self.assertEqual(actual_text_gd,expected_text_gd)

    def test_traduccion_idioma_irlandes_selenium(self):
        
        selector_de_idioma = self.driver.find_element(By.ID,"id_language")

        #cambiamos al idioma irlandes
        self.selector_idioma(selector_de_idioma,"ga")

        #comprueba la traduccion al irlandes
        expected_text_ga = "Taifead"
        element_ga = self.driver.find_element(By.TAG_NAME, "h2")
        actual_text_ga = element_ga.text
        self.assertEqual(actual_text_ga,expected_text_ga)

    def test_traduccion_idioma_gallego_selenium(self):
        
        selector_de_idioma = self.driver.find_element(By.ID,"id_language")

        #cambiamos al idioma gallego
        self.selector_idioma(selector_de_idioma,"gl")

        #comprueba la traduccion al gallego
        expected_text_gl = "Gravar"
        element_gl = self.driver.find_element(By.TAG_NAME, "h2")
        actual_text_gl = element_gl.text
        self.assertEqual(actual_text_gl,expected_text_gl)

    def test_traduccion_idioma_italiano_selenium(self):
        
        selector_de_idioma = self.driver.find_element(By.ID,"id_language")

        #cambiamos al idioma italiano
        self.selector_idioma(selector_de_idioma,"it")

        #comprueba la traduccion al italiano
        expected_text_it = "Documentazione"
        element_it = self.driver.find_element(By.TAG_NAME, "h2")
        actual_text_it = element_it.text
        self.assertEqual(actual_text_it,expected_text_it)

    def test_traduccion_idioma_turco_selenium(self):
        
        selector_de_idioma = self.driver.find_element(By.ID,"id_language")

        #cambiamos al idioma turco
        self.selector_idioma(selector_de_idioma,"tr")

        #comprueba la traduccion al turco
        expected_text_tr = "Kayıt"
        element_tr = self.driver.find_element(By.TAG_NAME, "h2")
        actual_text_tr = element_tr.text
        self.assertEqual(actual_text_tr,expected_text_tr)

    def test_traduccion_idioma_portugues_selenium(self):
        
        selector_de_idioma = self.driver.find_element(By.ID,"id_language")

        #cambiamos al idioma portugues
        self.selector_idioma(selector_de_idioma,"pt")

        #comprueba la traduccion al portugues
        expected_text_pt = "Registro"
        element_pt = self.driver.find_element(By.TAG_NAME, "h2")
        actual_text_pt = element_pt.text
        self.assertEqual(actual_text_pt,expected_text_pt)

    def test_traduccion_idioma_catalan_selenium(self):
        
        selector_de_idioma = self.driver.find_element(By.ID,"id_language")

        #cambiamos al idioma catalan
        self.selector_idioma(selector_de_idioma,"ca")

        #comprueba la traduccion al catalan
        expected_text_ca = "Registre"
        element_ca = self.driver.find_element(By.TAG_NAME, "h2")
        actual_text_ca = element_ca.text
        self.assertEqual(actual_text_ca,expected_text_ca)

    def test_traduccion_idioma_aleman_selenium(self):
        
        selector_de_idioma = self.driver.find_element(By.ID,"id_language")

        #cambiamos al idioma aleman
        self.selector_idioma(selector_de_idioma,"de")

        #comprueba la traduccion al aleman
        expected_text_de = "Aufzeichnen"
        element_de = self.driver.find_element(By.TAG_NAME, "h2")
        actual_text_de = element_de.text
        self.assertEqual(actual_text_de,expected_text_de)


    def selector_idioma(self, selector,language_id):
        #se usa select para usar el elemento select de la pagina
        select = Select(selector)
        #se escoge el idioma segun el id dado
        select.select_by_value(language_id)

    def tearDown(self):
        #se cierra chrome
        self.driver.quit()


