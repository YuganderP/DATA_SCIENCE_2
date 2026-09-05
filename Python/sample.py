import requests
import time
import asyncio


async def fetch_data(name, url):
    data = await asyncio.to_thread(requests.get, url)
    return data.json()


one = "https://official-joke-api.appspot.com/random_joke"
two = "https://catfact.ninja/fact"
three = "https://api.restful-api.dev/objects/1"


async def main():
    result = await asyncio.gather(
        fetch_data("one", one), fetch_data("two", two), fetch_data("three", three)
    )
    for i in result:
        print(i)


asyncio.run(main())
