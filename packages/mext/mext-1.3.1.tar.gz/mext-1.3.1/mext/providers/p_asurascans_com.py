from mext.providers.bases.base_mangastream_wp import MangaStreamBase


class AsuraScansCom(MangaStreamBase):

    def __init__(self, name, siteUrl):
        self.language = 'en'
        super(AsuraScansCom, self).__init__(name, siteUrl)
