#!/usr/bin/env python3
# -*-  coding: utf-8 -*-

import logging
import os
import time

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.remote_connection import LOGGER
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait, Select

LOGGER.setLevel(logging.WARNING)


class SdetWebDriver():
    def __init__(self):
        self.web_driver = webdriver
        self.timeout = 10
        self.short_timeout = 2
        self.screenshot_path = os.getcwd() + '/screenshot/'

    def sdet_open_browser(self):
        logging.debug('sdet_open_browser')
        chrome_options = self._get_chrome_options()
        self.web_driver = webdriver.Chrome(executable_path='./chromedriver', options=chrome_options)
        self.web_driver.implicitly_wait(self.timeout)

    def _get_chrome_options(self):
        chrome_options = Options()
        # chrome_options.add_experimental_option(
        #     'prefs', {'safebrowsing.enabled': True, 'download.default_directory': f"{TEST_DATA_DIR}"})
        chrome_options.add_argument('--ignore-certificate-errors')
        chrome_options.add_experimental_option('excludeSwitches', ['enable-automation', 'enable-logging'])
        # Disable sandbox mode. Resolve error when DevToolsActivePort file does not exist
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')  # Overcome limited resources [for Linux only]
        
        # chrome_options.add_argument('--headless')
        chrome_options.add_argument("--window-size=1440,768")
        chrome_options.add_argument('--disable-gpu')
        # chrome_options.add_argument('blink-settings=imagesEnabled=false')
        return chrome_options

    def sdet_save_screenshot(self, filename):
        logging.debug(f'sdet_save_screenshot: {filename}')
        self.web_driver.save_screenshot(self.screenshot_path + filename + '.png')

    def sdet_click_element(self, locator, timeout=None):
        _status = 'Failed'
        if timeout is None:
            timeout = self.timeout
        try:
            element = WebDriverWait(self.web_driver, timeout, 1).until(
                EC.element_to_be_clickable((By.XPATH, locator))
            )
            element = WebDriverWait(self.web_driver, timeout, 1).until(
                EC.presence_of_element_located((By.XPATH, locator))
            )
            element.click()
            _status = 'Success'
        except TimeoutException as ex:
            logging.debug(f'sdet_click_element: {locator}, timeout')
        finally:
            logging.debug(f'sdet_click_element: {locator}, status: {_status}')

    def sdet_check_element_exists(self, locator, timeout=10):
        result = False
        try:
            element = WebDriverWait(self.web_driver, timeout).until(
                EC.presence_of_element_located((By.XPATH, locator))
            )
        except TimeoutException as ex:
            logging.debug(f'sdet_click_element: {locator}, timeout')
            result = False
        else:
            result = True
        finally:
            logging.debug('sdet_check_element_exists, locator: %s, exists: %s' % (locator, result))
        return result

    def sdet_fill_text(self, locator, text):
        try:
            element = WebDriverWait(self.web_driver, self.timeout).until(
                EC.presence_of_element_located((By.XPATH, locator))
            )
            # element.send_keys(Keys.CONTROL + "a")
            # element.clear()
            element.send_keys(text)
        except TimeoutException as ex:
            logging.debug(f'sdet_click_element: {locator}, timeout')
        finally:
            logging.debug('sdet_fill_text locator: %s, text: %s' % (locator, text))

    def sdet_get_text(self, locator):
        logging.debug(f'sdet_click_element: {locator}, timeout')
        result = ''
        try:
            element = WebDriverWait(self.web_driver, self.timeout).until(
                EC.presence_of_element_located((By.XPATH, locator))
            )
            result = element.text
        except TimeoutException as ex:
            logging.debug(f'sdet_click_element: {locator}, timeout')

        return result

    def sdet_scroll_to(self, locator):
        element = self.web_driver.find_element(By.XPATH, locator)
        self.web_driver.execute_script("arguments[0].scrollIntoView();", element)
        logging.debug('sdet_scroll_to element: %s' % locator)
        time.sleep(2)


if __name__ == "__main__":
    logging.debug('sdet_common')
    # browser = 'chrome'
    # driver_instance = SdetWebDriver(browser)
    # driver_instance.web_driver.get('https://www.google.com')
    # driver_instance.web_driver.close()
