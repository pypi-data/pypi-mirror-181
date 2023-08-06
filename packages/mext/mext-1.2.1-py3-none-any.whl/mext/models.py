import io

from typing import List
from datetime import datetime

from mext import enums


class Model:

    def __init__(self, provider):
        self.name = provider.name

    @property
    def __dict__(self):
        return self.to_dict()

    def __iter__(self):
        for field in self.__slots__:
            yield (field, getattr(self, field))

    def __str__(self):
        return "{} {}".format(self.name, self.__class__.__name__)

    def to_dict(self):
        return {field: getattr(self, field) for field in self.__slots__}


class Cover(Model):
    """Represents a Cover."""
    __slots__ = (
        "id", "description", "volume", "file_bytes", "url", "url_256", "url_512",
        "provider", "instance"
    )

    def __init__(self, provider):
        super().__init__(provider)
        self.id: str = None
        self.description: str = ""
        self.volume: float = float(0)
        self.file_bytes: io.BytesIO = io.BytesIO()
        self.url: str = ""
        self.url_256: str = ""
        self.url_512: str = ""
        self.provider = provider
        self.instance = self

    def __str__(self) -> str:
        return self.url

    def __repr__(self) -> str:
        return str(self)

    def get_url(self):
        return self.url | self.url_512 | self.url_256 | ""


class Tag(Model):
    """Represents a Manga Tag."""
    __slots__ = (
        "id", "name", "description", "url",
        "provider", "instance"
    )

    def __init__(self, provider):
        super().__init__(provider)
        self.id: str = None
        self.name: str = ""
        self.description: str = ""
        self.url: str = ""
        self.provider = provider
        self.instance = self

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return str(self)


class Genre(Model):
    """Represents a Manga Tag."""
    __slots__ = (
        "id", "name", "description", "url",
        "provider", "instance"
    )

    def __init__(self, provider):
        super().__init__(provider)
        self.id: str = None
        self.name: str = ""
        self.description: str = ""
        self.url: str = ""
        self.provider = provider
        self.instance = self

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return str(self)


class Person(Model):
    """Represents a Author or Artist or any related Person"""
    __slots__ = (
        "id", "name", "image", "bio", "url",
        "provider", "instance",
    )

    def __init__(self, provider):
        super().__init__(provider)
        self.id: str = None
        self.name: str = ""
        self.image: str = ""
        self.bio: str = ""
        self.url: str = ""
        self.provider = provider
        self.instance = self

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return str(self)


class Manga(Model):
    """Represents a Manga."""
    __slots__ = (
        "id", "title", "alts", "description", "links", "language", "comic_type", "status",
        "year", "rating", "followers", "genres", "tags", "authors", "artists", "current_cover",
        "all_covers", "banner_picture", "adult", "first_chapter", "last_chapter", "chapter_list",
        "url", "created_at", "updated_at", "provider", "instance"
    )

    def __init__(self, provider):
        super().__init__(provider)
        self.id: str = ""
        self.title: str = ""
        self.alts: List[str] = []
        self.description: str = ""
        self.links: List[str] = []
        self.language: enums.ComicTypesLanguage = None
        self.comic_type: str = ""
        self.status: enums.StatusTypes = None
        self.year: int = datetime.now().year
        self.rating: float = float(0)
        self.followers: int = int(0)
        self.genres: List[Genre] = []
        self.tags: List[Tag] = []
        self.authors: List[Person] = []
        self.artists: List[Person] = []
        self.current_cover: Cover = None
        self.all_covers: List[Cover] = []
        self.banner_picture: str = ""
        self.adult: bool = False
        self.first_chapter: Chapter = None
        self.last_chapter: Chapter = None
        self.chapter_list: List[Chapter] = []
        self.url: str = ""
        self.created_at: datetime = None
        self.updated_at: datetime = None
        self.provider = provider
        self.instance = self

    def __str__(self) -> str:
        return self.title

    def __repr__(self) -> str:
        return str(self)


class Page(Model):
    """Represents a Page"""
    __slots__ = (
        "url",
        "provider", "instance"
    )

    def __init__(self, provider):
        super().__init__(provider)
        self.url: str = ""

    def __str__(self) -> str:
        return self.url

    def __repr__(self) -> str:
        return self.url


class Chapter(Model):
    """Represents a Chapter."""
    __slots__ = (
        "id", "name", "number", "volume", "language", "special", "pages",
        "manga", "group", "uploader", "url", "created_at", "updated_at",
        "provider", "instance"
    )

    def __init__(self, provider):
        super().__init__(provider)
        self.id: str = ""
        self.name: str = ""
        self.number: str = ""
        self.volume: float = float(0)
        self.language: str = ""
        self.special: bool = False
        self.pages: List[Page] = ""
        self.manga: Manga = None
        self.group: str = None
        self.uploader: str = None
        self.url: str = ""
        self.created_at: datetime = None
        self.updated_at: datetime = None
        self.provider = provider
        self.instance = self

    def __str__(self) -> str:
        srep = f"Chapter {self.number}"
        if self.name:
            srep = f"{srep} - {self.name}"
        return srep

    def __repr__(self) -> str:
        return str(self)
