import re

from datetime import datetime
from urllib.parse import ParseResult, urlencode, urlparse, urlunparse

from bs4 import BeautifulSoup

from mext import enums, models, client, utils
from mext.provider import Provider


class ReaperScansCom(Provider):

    def __init__(self, name, siteUrl):
        self.language = 'en'
        super(ReaperScansCom, self).__init__(name, siteUrl)

    def get_latest(self, url, page):
        return

    def get_manga(self, url, page):

        self.selenium.get_cfpage(url)
        self.find_error(url)

        manga = models.Manga(self)
        manga.url = url

        soup = BeautifulSoup(self.selenium.source, 'lxml')

        wrong_field_values = ['-', 'N/A']

        # Description
        description_element = soup.select_one('p[tabindex="0"]')

        description_text = description_element.text if description_element else ''
        if description_text:
            trans = description_text.maketrans({
                "‘": "'",
                "’": "'",
                "“": "'",
                "”": "'",
            })
            manga.description = description_text.strip()\
                .translate(trans)

        other_elements_selector = "body > div.flex.flex-col.h-screen.justify-between > main > div.mx-auto.py-8.grid.max-w-3xl.grid-cols-1.gap-4.sm\\:px-6.lg\\:max-w-screen-2xl.lg\\:grid-flow-col-dense.lg\\:grid-cols-3 > section > div:nth-child(1) > div > div > dl > div"
        other_elements = soup.select(other_elements_selector)

        for metadata_element in other_elements:

            if metadata_element:
                field_name_element = metadata_element.select_one('dt')
                if field_name_element:
                    if field_name_element.string:
                        field_name = field_name_element.string
                    else:
                        field_name = field_name_element.text

                    field_name = field_name.strip()
                else:
                    continue

                field_value_element = metadata_element\
                    .select_one('dd')
                if field_value_element:
                    if field_value_element.string:
                        field_value = field_value_element.string.strip()
                    else:
                        field_value = field_value_element.text.strip()

                    field_value = field_value.strip()

                    if field_value in wrong_field_values:
                        continue
                else:
                    continue
            else:
                continue

            # Status
            if field_name == 'Release Status':
                if field_value:
                    manga.status = enums.StatusTypes['Ongoing']

            # Type
            type_element = soup.select('div.tsinfo div.imptdt')[1]
            type_text = type_element\
                .select_one('a').string if type_element else ''
            if type_text:
                manga.comic_type = type_text

        return manga

    def get_chapter(self, *args, **kwargs):
        return super(ReaperScansCom, self).get_chapter(*args, **kwargs)

    def get_manga_chapters(self, *args, **kwargs):
        return super(ReaperScansCom, self).get_manga_chapters(*args, **kwargs)
