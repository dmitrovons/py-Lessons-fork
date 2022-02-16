#!/usr/bin/python3 -B

import os
import time
import asyncio
import aiohttp
from urllib.parse import urlparse
from bs4 import BeautifulSoup


class TScraper():
    def __init__(self, aUrl: str, aMaxConn = 64):
        self.Root = aUrl
        self.Url = []
        self.UrlErr = []
        self.MaxConn = aMaxConn
        self.TotalData = 0

    def _AddItem(self, aList: list, aUrl: str):
        if (not aUrl in aList):
            aList.append(aUrl)

    def _GetHeader(self):
        Res = {
            "Accept": "*/*",
            "User-Agent": "Mozilla/5.0 (iPad; CPU OS 11_0 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) Version/11.0 Mobile/15A5341f Safari/604.1"
        }
        return Res

    async def _GrabHref(self, aUrl: str, aData: str, aDepth: int):
        self.TotalData += len(aData)

        Hrefs = []
        Soup = BeautifulSoup(aData, "lxml")
        for A in Soup.find_all("a"):
            Href = A.get("href", '').strip().rstrip('/')
            if (Href):
                Path = urlparse(Href).path
                Ext = os.path.splitext(Path)[1]
  
                if (Href.startswith('/')):
                    Href = self.Root + Href

                if (Href.startswith(self.Root)) and \
                   (not Href.startswith('#')) and \
                   (not Href in Hrefs) and \
                   (not Ext in ['.zip', '.jpg']):
                    self._AddItem(Hrefs, Href)
        await self._ParseRecurs(Hrefs, aDepth + 1)

    async def _Fetch(self, aUrl: str, aSession, aSemaph, aDepth: int):
        async with aSemaph:
            try:
                async with aSession.get(aUrl) as Response:
                    Data = await Response.read()
                    if (Data):
                        await self._GrabHref(aUrl, Data, aDepth)
            except aiohttp.ClientConnectorError as E:
                self.Url.remove(aUrl)
                self._AddItem(self.UrlErr, aUrl)
                print('Error', E, aUrl)

    async def _ParseRecurs(self, aUrl: list, aDepth: int):
        async with aiohttp.ClientSession(headers=self._GetHeader()) as Session:
            Semaph = asyncio.Semaphore(self.MaxConn)

            Tasks = []
            for Url in aUrl:
                if (not Url in self.Url):
                    self.Url.append(Url)
                    print('---x1. Depth: %d, URLs: %d, Total: %dM, URL: %s' % (aDepth, len(self.Url), self.TotalData / 1000000, Url))

                    Task = asyncio.create_task(self._Fetch(Url, Session, Semaph, aDepth))
                    Tasks.append(Task)
            await asyncio.gather(*Tasks)


class TMain():
    def __init__(self):
        pass

    async def _Scheduler(self, aUrl: str, aSemaph):
        async with aSemaph:
            Scraper = TScraper(aUrl, 8)
            await Scraper._ParseRecurs([aUrl], 0)
            print('url: %s, count: %d, size: %d' % (Url, len(Scraper.Url), Scraper.TotalData))

    async def CreateTasks(self, aUrl: list, aMaxTasks: int):
        Semaph = asyncio.Semaphore(aMaxTasks)

        Tasks = []
        for Url in aUrl:
            if (not Url.startswith('-')):
                Task = asyncio.create_task(self._Scheduler(Url, Semaph))
                Tasks.append(Task)
        await asyncio.gather(*Tasks)

    def Run(self, aUrl: list, aMaxTasks: int = 3):
        Task = self.CreateTasks(aUrl, aMaxTasks)
        asyncio.run(Task)


Url = ['https://www.neotec.ua', 'https://largo.com.ua', 'http://oster.com.ua', 'http://bereka-radio.com.ua', 'https://kaluna.te.ua']
StartT = time.time()
Main = TMain()
Main.Run(Url, 5)
print('duration (s)', round(time.time() - StartT, 2))
