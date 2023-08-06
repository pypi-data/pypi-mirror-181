import os

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

import undetected_chromedriver as uc


class ChromeDriver:
    arguments = []
    _driver = None

    def __init__(self, arguments: list = []):
        self.arguments = arguments
    
    def _make_driver(self):

        self.capabilities = DesiredCapabilities.CHROME.copy()
        self.capabilities['goog:loggingPrefs'] = {'performance': 'ALL'}

        self.options = uc.ChromeOptions()
        self.options.headless = False

        if self.arguments:
            argument_list = self.arguments
        else:
            argument_list = [
                # '--no-sandbox', # Insecure
                '--mute-audio',
                '--disable-gpu',
                '--no-first-run',
                '--disable-extensions'
                '--no-service-autorun',
                '--password-store=basic',
                # '--disable-dev-shm-usage',
                '--disable-blink-features',
                '--disable-blink-features=AutomationControlled',
            ]
        self.options.arguments.extend(argument_list)

        self._driver = uc.Chrome(
            options=self.options,
            desired_capabilities=self.capabilities
        )
    
    def init_driver(self):
        if not self._driver:
            self._make_driver()
        return self

    def get_page(self, url, *args, **kwargs):
        return self._driver.get(url, *args, **kwargs)

    def get_cfpage(self, url, *args, **kwargs):
        page = self.get_page(url, *args, **kwargs)

        WebDriverWait(self._driver, 15).until_not(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, 'p[data-translate=resolve_captcha_network]')
            )
        )

        return page

    @property
    def source(self):
        return self._driver.page_source

    def __del__(self):
        if self._driver:
            self.exit()

    def exit(self):
        self._driver.quit()