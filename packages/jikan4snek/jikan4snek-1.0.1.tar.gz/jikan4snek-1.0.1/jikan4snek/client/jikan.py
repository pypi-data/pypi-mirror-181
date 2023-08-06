from typing import Union
from ..base.fetch import request
from ..base.constant import Api

Jikan = Api()


class Jikan4SNEK(object):
    """Jikan4SNEK Constructor 

    You may want to running your own instance [jikan-me/jikan](https://github.com/jikan-me/jikan) or [jikan-me/jikan-rest](https://github.com/jikan-me/jikan-rest)
    Jikan4SNEK apply customizable: `api_url`, `user-agent`, and `base expiration cache`.

    Parameters
    ----------
    ua : dict
        Your custom user agent. Default is `jikan4snek/v{__version__}`
    api : str
        Custom jikan api url. Default is https://api.jikan.moe/v4
    purge_cache : int
        Purge the whole cache after x minutes. Default is 60 minutes.
        PS: Your cache will never be purged if you dont have any process running.
    """

    def __init__(
        self,
        ua: dict = Jikan.headers,
        api: str = Jikan.api,
        purge_cache: int = Jikan.expire_cache,
    ):

        self.ua = ua
        self.api = api
        self.purge_cache = purge_cache

    @staticmethod
    async def fetch_aiosequel(
        self, path: str, entry: str = "", eps: str = ""
    ) -> Union[dict, None]:
        """Check table if the data is cached, if not, fetch the data from the API.

        Parameters
        ----------
        path : str
            The path to the API.
        entry : str
            The entry path after "/".
        eps : str
            The episode number (if the entry is "episodes")

        Returns
        -------
        Union[dict, None]
            The response cache or api
        """
        raw_data = await request(
            api=self.api,
            purge_cache=self.purge_cache,
            ua=self.user_agent,
            someid=self.id,
            path=path,
            entry=entry,
            eps=eps,
        )
        return raw_data

    def get(
        self, some_id: int, entry: str = "", eps: str = ""
    ) -> "JikanResponseFromId":
        ##print(some_id, entry, eps)
        ##print(self.ua)
        """
        Returns the JikanResponseFromId object.

        Parameters
        ----------
        some_id : int
            The id what you want to get.

        entry : str
            The entry path, default is empty which means "/".

        eps : str
            The episode number (only consume if the entry is "episodes").

        """
        return JikanResponseFromId(self, some_id, entry, eps)

    def search(self, query: str, limit: int = 25, page: int = 1) -> "JikanResponseFromSearch":
        """Returns the JikanResponseFromSearch object.

        Parameters
        ----------
        query : str
            The query what you want to search.

        limit : int
            The limit of the search result. Default is 25.

        page : int
            The page of the search result. Default is 1.
        """
        return JikanResponseFromSearch(self, query, limit, page)


class JikanResponseFromId:
    ## object utama
    def __init__(self, raw_, id_, entry_: str = "", eps_: str = ""):
        self.id = id_
        self.entry = entry_
        self.eps = eps_
        self.raw = raw_
        self.api = raw_.api
        self.user_agent = raw_.ua
        self.purge_cache = raw_.purge_cache
        ##print(self.id, self.raw)

    async def anime(self):
        """Returns the anime data.

        Returns
        -------
        Union[dict, None]
            The response from the API.
        """
        ##return self
        ## 'entry': 'episodes'

        if self.entry and self.entry not in Jikan.anime_valid_entries:
            raise ValueError(f"Invalid entry {Jikan.anime_valid_entries}")
        elif self.entry == "episodes":
            return await Jikan4SNEK.fetch_aiosequel(self, "anime", self.entry, self.eps)
        elif self.entry == "videos_episodes":
            return await Jikan4SNEK.fetch_aiosequel(self, "anime", "videos", "episodes")

        return await Jikan4SNEK.fetch_aiosequel(self, "anime", self.entry)

    async def manga(self):
        """
        Returns the manga data.

        Returns
        -------
        Union[dict, None]
            The response from the API.
        """
        if self.entry and self.entry not in Jikan.manga_valid_entries:
            raise ValueError(f"Invalid entry {Jikan.manga_valid_entries}")

        return await Jikan4SNEK.fetch_aiosequel(self, "manga", self.entry)

    async def characters(self):
        """
        Returns the character data.

        Returns
        -------
        Union[dict, None]
            The response from the API.
        """
        if self.entry and self.entry not in Jikan.character_valid_entries:
            raise ValueError(f"Invalid entry {Jikan.character_valid_entries}")

        return await Jikan4SNEK.fetch_aiosequel(self, "characters", self.entry)

    async def clubs(self):
        """
        Returns the club data.

        Returns
        -------
        Union[dict, None]
            The response from the API.
        """
        if self.entry and self.entry not in Jikan.club_valid_entries:
            raise ValueError(f"Invalid entry {Jikan.club_valid_entries}")

        return await Jikan4SNEK.fetch_aiosequel(self, "clubs", self.entry)

    async def people(self):
        """
        Returns the people data.

        Returns
        -------
        Union[dict, None]
            The response from the API.
        """
        if self.entry and self.entry not in Jikan.people_valid_entries:
            raise ValueError(f"Invalid entry {Jikan.people_valid_entries}")

        return await Jikan4SNEK.fetch_aiosequel(self, "people", self.entry)

    async def producers(self):
        """
        Returns the producer data.

        Returns
        -------
        Union[dict, None]
            The response from the API.
        """
        if self.entry and self.entry not in Jikan.producer_valid_entries:
            raise ValueError(f"Invalid entry {Jikan.producer_valid_entries}")

        return await Jikan4SNEK.fetch_aiosequel(self, "producers", self.entry)

    async def random(self):
        """
        Returns the random data.

        Returns
        -------
        Union[dict, None]
            The response from the API.
        """
        if self.id not in Jikan.random_valid_id_not_entries:
            raise ValueError(f"Invalid entry {Jikan.random_valid_id_not_entries}")

        return await Jikan4SNEK.fetch_aiosequel(self, "random", self.entry)

    async def users(self):
        """
        Returns the user data.

        Returns
        -------
        Union[dict, None]
            The response from the API.
        """
        if self.entry and self.entry not in Jikan.user_valid_entries:
            raise ValueError(f"Invalid entry {Jikan.user_valid_entries}")

        return await Jikan4SNEK.fetch_aiosequel(self, "users", self.entry)


class JikanResponseFromSearch:
    def __init__(self, raw_, query, limit_, page_):
        self.id = query
        self.limit = limit_
        self.page = page_
        self.raw = raw_
        self.api = raw_.api
        self.user_agent = raw_.ua
        self.purge_cache = raw_.purge_cache
        ##print(self.__dict__)

    async def anime(self):
        """Search the anime data.

        Returns
        -------
        Union[dict, None]
            The response search from the API.
        """
        return await Jikan4SNEK.fetch_aiosequel(
            self, f"anime?q={self.id}&limit={self.limit}&page={self.page}"
        )

    async def manga(self):
        """Search the manga data.

        Returns
        -------
        Union[dict, None]
            The response search from the API.
        """
        return await Jikan4SNEK.fetch_aiosequel(
            self, f"manga?q={self.id}&limit={self.limit}&page={self.page}"
        )

    async def characters(self):
        """Search the characters data.

        Returns
        -------
        Union[dict, None]
            The response search from the API.
        """
        return await Jikan4SNEK.fetch_aiosequel(
            self, f"characters?q={self.id}&limit={self.limit}&page={self.page}"
        )

    async def clubs(self):
        """Search the clubs data.

        Returns
        -------
        Union[dict, None]
            The response search from the API.
        """
        return await Jikan4SNEK.fetch_aiosequel(
            self, f"clubs?q={self.id}&limit={self.limit}&page={self.page}"
        )

    async def people(self):
        """Search the people data.

        Returns
        -------
        Union[dict, None]
            The response search from the API.
        """
        return await Jikan4SNEK.fetch_aiosequel(
            self, f"people?q={self.id}&limit={self.limit}&page={self.page}"
        )

    async def producers(self):
        """Search the producers data.

        Returns
        -------
        Union[dict, None]
            The response search from the API.
        """
        return await Jikan4SNEK.fetch_aiosequel(
            self, f"producers?q={self.id}&limit={self.limit}&page={self.page}"
        )

    async def magazines(self):
        """Search the magazines data.

        Returns
        -------
        Union[dict, None]
            The response search from the API.
        """
        return await Jikan4SNEK.fetch_aiosequel(
            self, f"magazines?q={self.id}&limit={self.limit}&page={self.page}"
        )