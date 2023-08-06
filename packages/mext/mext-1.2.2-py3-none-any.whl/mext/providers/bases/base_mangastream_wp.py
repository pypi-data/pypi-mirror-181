import re

from datetime import datetime
from urllib.parse import ParseResult, urlencode, urlparse, urlunparse

from bs4 import BeautifulSoup

from mext import enums, models, client, utils
from mext.provider import Provider


class MangaStreamBase(Provider):

    def __init__(self, name, siteUrl):
        self.name = name
        super(MangaStreamBase, self).__init__(name, siteUrl)

    def process_chapter_name(self, chapter_text):
        chapter_number, chapter_name = None, ''
        if chapter_text:
            chapter_text = chapter_text.strip()

            match_patterns = [
                r'preview|promotional\s+video', 
                r'([0-9]*[.]?[0-9]+)\s*\-?\s*(.*)'
            ]
            if re.search(match_patterns[0], chapter_text, re.IGNORECASE):
                chapter_name = chapter_text
                chapter_number = float(0)

            elif re.search(match_patterns[1], chapter_text):
                rsearch = re.search(match_patterns[1], chapter_text)
                len_rsearch = len(rsearch.groups())

                if len_rsearch > 0 and rsearch.group(1):
                    chapter_number = rsearch.group(1)

                    if len_rsearch > 1 and rsearch.group(2):
                        chapter_name = rsearch.group(2)

            chapter_number = chapter_number \
                if chapter_number not in [None, ''] \
                else chapter_text

            try:
                chapter_number = float(chapter_number)
            except:
                print(
                    f"Error getting chapter number for text {chapter_text}"
                )
        else:
            chapter_number = None

        return chapter_number, chapter_name

    @utils.data_page
    def get_latest(self, url, page):

        parsed_url = urlparse('/'.join(url.split('/')[0:3]))

        pr = ParseResult(
            scheme=parsed_url.scheme,
            netloc=parsed_url.netloc,
            path='/manga/',
            params='',
            query=urlencode({'page': page, 'order': 'update'}),
            fragment=''
        )

        mangalist_url = urlunparse(pr)

        self.selenium.get_cfpage(mangalist_url)
        self.find_error(mangalist_url)

        latest_list = []

        soup = BeautifulSoup(self.selenium.source, 'lxml')

        listing_element = soup.select_one('div.mrgn div.listupd')

        if listing_element:

            for update_element in listing_element.select('div.bs'):
                if update_element:
                    manga = models.Manga(self)

                    url_element = update_element.select_one(
                        'div.bsx > a[href][title]')
                    if url_element:
                        manga.url = url_element.attrs['href']

                    cover_element = update_element.select_one(
                        'div.limit > img.ts-post-image[alt][src]')
                    if cover_element:
                        cover = models.Cover(self)
                        cover.url = cover_element.attrs['src']
                        manga.all_covers.append(cover)
                        manga.current_cover = manga.all_covers[-1]

                    type_element = update_element.select_one('span.type')
                    type_text = type_element.string if type_element else ''
                    if type_text:
                        manga.comic_type = type_text

                    title_element = update_element.select_one(
                        'div.bigor > div.tt')
                    title_text = title_element.string if title_element else ''
                    if title_text:
                        manga.title = title_text.strip()
                    else:
                        raise Exception(
                            'Could not find comic title for one of the comics')

                    chapter_element = update_element.select_one(
                        'div.bigor div.epxs')
                    chapter_text = chapter_element.string if chapter_element else ''
                    chapter_number = re.findall(
                        'Chapter (\d+)', chapter_text) if chapter_text else ''

                    if chapter_number:
                        latest_chapter = models.Chapter(self)
                        latest_chapter.number = str(float(chapter_number[0]))
                        manga.last_chapter = latest_chapter

                latest_list.append(manga)

        return latest_list

    @utils.data_page
    def get_manga(self, url, page):

        self.selenium.get_cfpage(url)
        self.find_error(url)

        manga = models.Manga(self)
        manga.url = url

        soup = BeautifulSoup(self.selenium.source, 'lxml')

        wrong_field_values = ['-', 'N/A']

        # ID
        id_element = soup.select_one('div.rt div.bookmark[data-id]')

        if id_element:
            id_text = id_element.attrs['data-id']

            if id_text:
                manga.id = id_text.strip()

        # Cover
        thumb_element = soup.select_one(
            'div.thumb[itemtype="https://schema.org/ImageObject"] > img[itemprop="image"]'
        )

        if thumb_element:
            thumb_url = thumb_element.attrs.get('src')

            if thumb_url:
                cover = models.Cover(self)
                cover.url = thumb_url.strip()
                manga.current_cover = cover
                manga.all_covers.append(cover)

        # Background Image
        bg_element = soup.select_one(
            'div.bigcover div.ime img[src]'
        )

        if bg_element and bg_element.attrs.get('src'):
            manga.banner_picture = bg_element.attrs.get('src').strip()

        # Title
        title_element = soup.select_one('h1.entry-title')

        title_text = title_element.string if title_element else ''
        if title_text:
            trans = title_text.maketrans({
                "‘": "'",
                "’": "'",
                "“": "'",
                "”": "'",
            })
            manga.title = title_text.strip()\
                .translate(trans)
        else:
            raise Exception('Could not get title for comic')

        # Status
        status_element = soup.select('div.tsinfo div.imptdt')[0]

        status_text = status_element.select_one(
            'i').string if status_element else ''
        if status_text:
            manga.status = status_text

        # Type
        type_element = soup.select('div.tsinfo div.imptdt')[1]
        type_text = type_element.select_one('a').string if type_element else ''
        if type_text:
            manga.comic_type = type_text

        # Language
        if type_text:
            type_text = type_text.strip().lower()
            if type_text in enums.ComicTypesLanguage.dict():
                manga.language = enums.ComicTypesLanguage[type_text]

        # Alternative Titles
        alt_element = soup.select_one('div.infox div.wd-full')

        alt_names = []
        if alt_element and \
                alt_element.select_one('b') and \
                alt_element.select_one('b').string.strip() == 'Alternative Titles':
            alt_text = alt_element.select_one('span').string.strip()

            if alt_text and alt_text not in wrong_field_values:
                alt_delimiters = ['|', ',']
                for delimiter in alt_delimiters:
                    for alt_name in alt_text.split(delimiter):
                        alt_names.append(alt_name.strip())

                    if alt_names:
                        break

        manga.alts = alt_names

        # Description
        description_element = soup.select_one(
            'div.infox div.entry-content.entry-content-single'
        )

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

        for metadata_element in soup.select('div.infox div.fmed'):

            if metadata_element:
                field_name_element = metadata_element.select_one('b')
                if field_name_element:
                    if field_name_element.string:
                        field_name = field_name_element.string
                    else:
                        field_name = field_name_element.text

                    field_name = field_name.strip()
                else:
                    continue

                field_value_element = metadata_element\
                    .select_one('span')
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

            # Author
            if field_name == 'Author':
                author_names = []
                author_names_text = field_value

                for name in author_names_text.split('/'):
                    if name:
                        person = models.Person(self)
                        person.name = name.strip()
                        author_names.append(person)

                manga.authors = author_names

            # Artist
            if field_name == 'Artist':
                artist_names = []
                artist_names_text = field_value

                for name in artist_names_text.split('/'):
                    if name:
                        person = models.Person(self)
                        person.name = name.strip()
                        artist_names.append(person)

                manga.artists = artist_names

            # Posted On
            if field_name == 'Posted On':

                posted_on_dt = field_value_element\
                    .select_one('time').attrs.get('datetime')

                if posted_on_dt:
                    manga.created_at = datetime.fromisoformat(posted_on_dt)

            # Updated On
            if field_name == 'Updated On':

                updated_on_dt = field_value_element\
                    .select_one('time').attrs.get('datetime')

                if posted_on_dt:
                    manga.created_at = datetime.fromisoformat(updated_on_dt)

        # Genres
        genre_elements = soup.select('span.mgen > a')

        genres = []
        if genre_elements:
            for genre_element in genre_elements:
                name = genre_element.text.strip()
                if name:
                    genre = models.Genre(self)
                    genre.name = name
                    genres.append(genre)

        manga.genres = genres

        # Extra data

        # Followers
        followers_element = soup.select_one('div.rt div.bmc')

        if followers_element:
            followers_text = followers_element.text.strip()
            followers_find = re.findall(
                'Followed by ([\d]+) people', followers_text)

            if followers_find:
                manga.followers = int(followers_find[0])

        # Rating
        rating_element = soup.select_one(
            'div.rating div[itemprop="ratingValue"]')

        if rating_element:
            rating_text = rating_element.text.strip()

            if rating_text:
                manga.rating = float(rating_text)

        # Return complete Manga data
        return manga

    @utils.data_page
    def get_chapter(self, url, page):

        self.selenium.get_cfpage(url)
        self.find_error(url)

        chapter = models.Chapter(self)
        chapter.url = url

        soup = BeautifulSoup(self.selenium.source, 'lxml')

        breadcrumb_element = soup.select_one(
            'ol[itemtype="http://schema.org/BreadcrumbList"]')
        if breadcrumb_element:
            lis = breadcrumb_element.select('li[itemprop="itemListElement"]')

            title_element = lis[1]
            title_text = title_element\
                .select_one('span[itemprop="name"]').string if title_element else ''

            chapter_bc = lis[2]
            chapter_name_text = chapter_bc\
                .select_one('span[itemprop="name"]').string if chapter_bc else ''

            if title_text and chapter_name_text:
                chapter_text = chapter_name_text\
                    .strip().replace(title_text, "", 1).strip()
                chapter_text = re.findall(
                    r'(?:chapter)?\s*(.+)', chapter_text, re.IGNORECASE)
                    
                if chapter_text:
                    chapter_number, chapter_name = self.process_chapter_name(
                        chapter_text[0]
                    )

                    if chapter_number not in [None, '']:
                        chapter.number = str(chapter_number)
                    else:
                        raise Exception(
                            f"Error extracting chapter number from text text {chapter_text}"
                        )

                    if chapter_name:
                        chapter.name = str(chapter_name)
                else:
                    print('Chapter number not found in text {chapter_text}')

        pages = []
        pages_element = soup.select_one('div#readerarea')

        for page_element in pages_element.select('p > img[src][width][height]'):
            page_url = page_element.attrs['src']
            page = models.Page(self)
            page.url = page_url
            pages.append(page)

        chapter.pages = pages

        return chapter

    @utils.data_page
    def get_manga_chapters(self, url, page):

        self.selenium.get_cfpage(url)
        self.find_error(url)

        chapter_list = []

        soup = BeautifulSoup(self.selenium.source, 'lxml')

        chapters_element = soup.select_one('ul.clstyle')

        for chapter_element in chapters_element.select('li[data-num]'):
            chapter = models.Chapter(self)

            if chapter_element:

                chapter_url_element = chapter_element\
                    .select_one('div.eph-num > a')
                if chapter_url_element:
                    chapter.url = chapter_url_element.attrs['href']

                chapter_text = chapter_element.attrs['data-num']
                chapter_number, chapter_name = self.process_chapter_name(
                    chapter_text
                )

                if chapter_number not in [None, '']:
                    chapter.number = str(chapter_number)
                else:
                    continue

                if chapter_name:
                    chapter.name = str(chapter_name)

                date_element = chapter_element.select_one('span.chapterdate')
                date_text = date_element.string if date_element else ''
                if date_text:
                    chapter.created_at = datetime.strptime(
                        date_text, '%B %d, %Y')

            chapter_list.append(chapter)

        return chapter_list
