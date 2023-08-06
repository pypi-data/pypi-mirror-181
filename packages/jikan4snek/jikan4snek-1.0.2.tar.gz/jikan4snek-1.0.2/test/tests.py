import asyncio
import jikan4snek
import argparse
import time


class Client(object):
    def __init__(self):
        self.dump = jikan4snek.dump
        self.some_bunch_of_anime = [
            44511,
            50602,
            50172,
            49918,
            49596,
            41467,
            48316,
            49709,
            42962,
            47917,
            49891,
            50425,
            50710,
            49784,
            51098,
            49979,
            52046,
            52193,
            51128,
            48542,
            49828,
            51403,
            50205,
            50528,
            50590,
            51212,
            30455,
            50923,
            50348,
            51680,
        ]


Base = Client()

async def fetch():
    Jikan = jikan4snek.Jikan4SNEK()
    start = time.time()

    for i in Base.some_bunch_of_anime:
        res = await Jikan.get(i).anime()
        print(f"{res['data']['mal_id']}: {res['data']['title']}")

    print(
        f"GET {len(Base.some_bunch_of_anime)} request sequentially without cache, took: {(time.time() - start) / 60:.2f} minutes"
    )


parse = argparse.ArgumentParser(description="J4snek")
parse.add_argument("-anime", action="store_true")
args = parse.parse_args()


async def main():
    if args.anime:
        return await fetch()
    else:
        print("No arguments given")


if __name__ == "__main__":
    asyncio.run(main())