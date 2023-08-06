from asyncio import sleep
from aiohttp_client_cache import CachedSession, SQLiteBackend
from typing import Union
from .constant import Api

Jikan = Api()

api_hit = []


async def request(
    path: str,
    someid: int,
    entry: str,
    eps: str = "",
    api: str = Jikan.api,
    ua: dict = Jikan.headers,
    purge_cache: int = Jikan.expire_cache,
) -> Union[dict, None]:
    """Request method by id.

    Parameters
    ----------
    api : str
        The base url of the API.
    path : str
        The path to the API.
    someid : int
        The id of the anime or manga.
    entry : str
        The entry path after "/"
    ua : dict
        The user agent.
    purge_cache : int
        Expire cache in minutes.

    Returns
    -------
    Union[dict, None]
        The response from the API.
    """

    sequel_cfg = SQLiteBackend(
        cache_name="jikan4snek_cache/jikan4snek",
        expire_after=purge_cache * 60,
        allowed_codes=(200, 304),
        allowed_methods=["GET"],
        timeout=2.5,
    )

    ## if someid has "?q=" then it's a search
    if "?q=" in str(path):
        endpoint = f"{path}"

    else:
        endpoint = f"{path}/{someid}/{entry}/{eps}"

    async with CachedSession(cache=sequel_cfg) as session:

        async with session.get(f"{api}/{endpoint}", headers=ua) as resp:
            ## print(resp.status)

            try:
                if Jikan.stable_hit:
                    if resp.from_cache:
                        res = await resp.json()
                        return res
                    else:
                        await sleep(Jikan.rate_limit)
                        res = await resp.json()
                        return res

                else:
                    if resp.from_cache:
                        res = await resp.json()
                        return res

                    elif resp.from_cache is False and len(api_hit) < 3:
                        api_hit.append(1)
                        await sleep(1)
                        res = await resp.json()
                        ## print(f"ratelimit hit 1: {api_hit}")
                        return res

                    else:
                        api_hit.clear()
                        await sleep(0.8)
                        api_hit.append(1)
                        res = await resp.json()
                        ## print(f"ratelimit hit 2: {api_hit}")
                        return res

            except Exception as e:
                raise Exception(
                    f"{resp.status} | failed to get data from: {path} with: {someid} due to: {e}"
                )
