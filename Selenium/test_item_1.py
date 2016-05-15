# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re

class ItemTest1(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "http://noinventory.cloudapp.net"
        self.verificationErrors = []
        self.accept_next_alert = True

    def test_item_test1(self):
        driver = self.driver
        driver.get(self.base_url + "/items")
        driver.find_element_by_xpath("(//button[@type='button'])[2]").click()
        driver.find_element_by_id("id_nombre_item").clear()
        driver.find_element_by_id("id_nombre_item").send_keys("prueba selenium")
        driver.find_element_by_id("id_descripcion_item").clear()
        driver.find_element_by_id("id_descripcion_item").send_keys("descripcion del objeto con el que vamos a realizar las pruebas unitarias")
        Select(driver.find_element_by_id("id_tag1")).select_by_visible_text("Facultad de Ciencias")
        Select(driver.find_element_by_id("id_tag2")).select_by_visible_text("ORDENADOR CPU TORRE")
        Select(driver.find_element_by_id("id_tag3")).select_by_visible_text("POR REVISAR")
        driver.find_element_by_id("id_peso").clear()
        driver.find_element_by_id("id_peso").send_keys("3.3")
        driver.find_element_by_id("id_unidades").clear()
        driver.find_element_by_id("id_unidades").send_keys("6")
        Select(driver.find_element_by_id("id_tag1")).select_by_visible_text(u"Facultad de Psicología")
        driver.find_element_by_name("submit").click()
        driver.find_element_by_id("texto").clear()
        driver.find_element_by_id("texto").send_keys("prueba seleni")
        driver.find_element_by_id("busqueda").click()
        driver.find_element_by_xpath("(//button[@type='button'])[3]").click()
        self.assertRegexpMatches(self.close_alert_and_get_its_text(), r"^¿Estas seguro que deseas borrar los Items[\s\S]$")

    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e: return False
        return True

    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException as e: return False
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
