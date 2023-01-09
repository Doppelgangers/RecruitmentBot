import asyncio

import aiohttp
from bs4 import BeautifulSoup


async def get_vacancy():
    async with aiohttp.ClientSession() as session:
        response = await session.get("https://aozio.ru/career/job2/")
        html = await response.text()
        soup: BeautifulSoup = BeautifulSoup(html, "lxml")
        box = soup.find("div", {"class": "wysiwyg"})

        h = box.find_all("h3")
        h.pop(0)
        h = [value.text for value in h]

        vacancy_list = box.find_all("ul")
        vacancy_list = [[li.text for li in ul.find_all("li")] for ul in vacancy_list]

        if vacancy_list.__len__() == h.__len__():
            vacancy = [{"title" : h[num], "vacancy_list": vacancy_list[num]} for num in range(h.__len__())]
            return vacancy


if __name__ == '__main__':
    asyncio.run(get_vacancy())
