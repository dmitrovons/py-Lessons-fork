#!/usr/bin/python3 -B

import os
import time
import asyncio
import aiohttp
from urllib.parse import urlparse
from bs4 import BeautifulSoup


class TDownload():
    def __init__(self, aUrl: str, aMaxConn = 64):
        self.Root = aUrl
        self.Url = []
        self.MaxConn = aMaxConn
        self.TotalData = 0

    def GetHeader(self):
        Res = {
            "Accept": "*/*",
            "User-Agent": "Mozilla/5.0 (iPad; CPU OS 11_0 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) Version/11.0 Mobile/15A5341f Safari/604.1"
        }
        return Res

    async def GrabHref(self, aUrl: str, aData: str, aDepth: int):
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

                if (Href.startswith(self.Root)) and (not Href.startswith('#')) and (not Href in Hrefs) and (not Ext in ['.zip', '.jpg']):
                     Hrefs.append(Href)

        await self.ParseRecurs(Hrefs, aDepth + 1)

    async def Fetch(self, aUrl: str, aSession, aSemaph, aDepth: int):
        async with aSemaph:
            try:
                async with aSession.get(aUrl) as Response:
                    Data = await Response.read()
                    if (Data):
                        await self.GrabHref(aUrl, Data, aDepth)
            except aiohttp.ClientConnectorError as E:
                print('Error', E, aUrl)

    async def ParseRecurs(self, aUrl: list, aDepth: int):
        async with aiohttp.ClientSession(headers=self.GetHeader()) as Session:
            Semaph = asyncio.Semaphore(self.MaxConn)

            Tasks = []
            for Url in aUrl:
                if (not Url in self.Url):
                    self.Url.append(Url)
                    print('---x1. Depth: %d, URLs: %d, Total: %dM, URL: %s' % (aDepth, len(self.Url), self.TotalData / 1000000, Url))

                    Task = asyncio.create_task(self.Fetch(Url, Session, Semaph, aDepth))
                    Tasks.append(Task)
            await asyncio.gather(*Tasks)

    def Run(self):
        Task = self.ParseRecurs([self.Root], 0)
        asyncio.run(Task)
        print('url: %d, size: %d' % (len(self.Url), self.TotalData))



#Url = 'https://www.neotec.ua'
#Url = 'https://largo.com.ua'
Url = 'http://oster.com.ua'
#Url = 'http://bereka-radio.com.ua'

StartT = time.time()
Download = TDownload(Url, 16)
Download.Run()
print('duration (s)', round(time.time() - StartT, 2))
