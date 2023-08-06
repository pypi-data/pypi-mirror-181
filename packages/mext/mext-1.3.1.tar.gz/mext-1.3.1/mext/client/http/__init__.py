import cloudscraper


class Http:

    retry_count = 20
    _headers = {}
    proxies = {}
    referer = ''
    status_code = None
    user_agent = '{} {}'.format(
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0)',
        'Gecko/20100101 Firefox/91.0'
    )
    default_lang = 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3'
    webp_header = 'text/html,application/xhtml+xml,application/xml;q=1.0,image/webp,image/apng,*/*;q=1.0'

    def __init__(self) -> None:
        self.proxies = {}
        self.cookies = {}
        self._history = []
        self.scraper = cloudscraper.create_scraper()

    def request(self, url: str, headers: dict = {}, data=None, cookies: dict = {}, method: str = 'get', files=None, **kwargs):
        if not isinstance(headers, dict) or headers:
            headers = {}

        headers.setdefault('User-Agent', self.user_agent)
        if self.referer:
            headers.setdefault('Referer', self.referer)
        headers.setdefault('Accept-Language', self.default_lang)
        headers['Accept'] = self.webp_header

        return self.scraper.request(
            url=url,
            headers=headers,
            cookies=cookies,
            method=method,
            files=files,
            **kwargs
        )

    def get(self, url: str, headers: dict = {}, cookies: dict = {}, **kwargs):
        return self.request(
            url=url,
            headers=headers,
            cookies=cookies,
            method='get',
            **kwargs
        )

    def get_stream(self, url: str, headers: dict = {}, cookies: dict = {}, **kwargs):
        kwargs['stream'] = True
        return self.get(url, headers, cookies, **kwargs)

    def reset_proxy(self):
        self.proxies = {}

    def set_proxy(self, proxy):
        self.reset_proxy()
        if isinstance(proxy, dict):
            self.proxies['http'] = proxy.get('http', None)
            self.proxies['https'] = proxy.get('https', None)
        elif isinstance(proxy, str):
            self.proxies['http'] = proxy
