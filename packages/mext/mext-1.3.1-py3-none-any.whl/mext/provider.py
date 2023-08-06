from urllib.error import HTTPError
from urllib.parse import urlparse

from mext import client, utils


class Provider:

    def __init__(self, name, siteUrl):
        self.name = name
        self.siteUrl = siteUrl
        self.language = ''

        self.client = client.Client('http')

    def process_url(self, url):
        self.parsed_url = urlparse(url)
        self.scheme = self.parsed_url.scheme
        self.netloc = self.parsed_url.netloc
    
    # @utils.data_page
    def get_latest(self, attribute_name):
        """Gets list of updated mangas."""
        raise NotImplementedError

    # @utils.data_page
    def get_manga(self, attribute_name):
        """Gets a manga with a specific url."""
        raise NotImplementedError

    # @utils.data_page
    def get_manga_list(self, attribute_name):
        """Gets a list of Manga."""
        raise NotImplementedError

    # @utils.data_page
    def get_chapter(self, attribute_name):
        """Gets a chapter with a specific url."""
        raise NotImplementedError

    # @utils.data_page
    def get_manga_chapters(self, attribute_name):
        """Gets chapters associated with a specific Manga."""
        raise NotImplementedError
    
    def get_cover(self, attribute_name):
        """Gets cover data associated with a specific Manga."""

    def find_error(self, url):
        if self.client.is_selenium:
            logs = self.client.selenium._driver.get_log('performance')
            status_code = utils.get_status(logs)
        else:
            status_code = self.client.http.status_code

        http_error_msg = ""

        if isinstance(status_code, int):
            if 400 <= status_code < 500:
                http_error_msg = (
                    f"{status_code} Client Error for url: {url}"
                )

            elif 500 <= status_code < 600:
                http_error_msg = (
                    f"{status_code} Server Error for url: {url}"
                )

        if http_error_msg:
            raise HTTPError(url=url, code=status_code, msg=http_error_msg, hdrs=None, fp=None)
