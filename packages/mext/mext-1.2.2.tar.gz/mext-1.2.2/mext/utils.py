import json
import functools
from textwrap import wrap

from mext import enums


# Get Selenium Status Code

def get_status(logs):
    for log in logs:
        if log['message']:
            d = json.loads(log['message'])
            try:
                content_type = 'text/html' in d['message']['params']['response']['headers']['content-type']
                response_received = d['message']['method'] == 'Network.responseReceived'
                if content_type and response_received:
                    return d['message']['params']['response']['status']
            except:
                pass


# Decorator

def data_page(func):
    attr_name = enums.DatacallAttributes[func.__name__]

    @functools.wraps(func)
    def wrapper(instance, url, page=1, refresh=False):

        attr_value = getattr(instance, attr_name, None)

        try:
            if attr_value and refresh is False:
                return attr_value

            return_data = func(instance, url, page)

            instance.selenium.exit()

            setattr(instance, attr_name, return_data)
            return getattr(instance, attr_name)
        except Exception as e:
            raise e

    return wrapper
