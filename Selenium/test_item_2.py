# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re

class ItemTest2(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "http://noinventory.cloudapp.net"
        self.verificationErrors = []
        self.accept_next_alert = True

    def test_item_test2(self):
        driver = self.driver
        driver.get(self.base_url + "/")
        driver.find_element_by_link_text("Items").click()
        driver.find_element_by_xpath("(//button[@type='button'])[2]").click()
        driver.find_element_by_id("id_nombre_item").clear()
        driver.find_element_by_id("id_nombre_item").send_keys("item selemium")
        driver.find_element_by_id("id_descripcion_item").clear()
        driver.find_element_by_id("id_descripcion_item").send_keys("items para las segunda bateria de test con selenium")
        Select(driver.find_element_by_id("id_tag1")).select_by_visible_text(u"Facultad de Odontología")
        Select(driver.find_element_by_id("id_tag2")).select_by_visible_text("IMPRESORA")
        Select(driver.find_element_by_id("id_tag3")).select_by_visible_text("FUNCIONA")
        driver.find_element_by_id("id_peso").clear()
        driver.find_element_by_id("id_peso").send_keys("3")
        driver.find_element_by_id("id_unidades").clear()
        driver.find_element_by_id("id_unidades").send_keys("12")
        driver.find_element_by_name("submit").click()
        driver.find_element_by_id("addToCatalogo").click()
        driver.find_element_by_link_text("Catalogos").click()
        driver.find_element_by_css_selector("h4").click()
        driver.find_element_by_xpath("//div[@id='5738878527821fe126efe8cd']/a[2]/button").click()

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
