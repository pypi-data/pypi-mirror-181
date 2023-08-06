from .http import Http
from . import selenium as Selenium

from mext import utils

class Client:
    http = None
    selenium = None

    def __init__(self, use_client='http') -> None:
        self.name = use_client

        if not use_client:
            raise Exception(
                "Error initializing client, use_client value not supported : {}".format(use_client)
            )
        elif use_client == 'selenium':
            Selenium.make_driver(browser='chrome')
            self.selenium = Selenium.get_driver()
        else:
            self.http = Http()
    
    @property
    def is_http(self):
        return self.name == 'http'
    
    @property
    def is_selenium(self):
        return self.name == 'selenium'
    
    @property
    def status_code(self):
        status_code = None
        if self.is_selenium:
            logs = self.selenium._driver.get_log('performance')
            status_code = utils.get_status(logs)
        else:
            self.http.status_code
