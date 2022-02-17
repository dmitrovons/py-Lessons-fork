#!/usr/bin/python3 -B


import os
import asyncio
import aiohttp
import time
from datetime import datetime
from random import randint
from urllib.parse import urlparse
from bs4 import BeautifulSoup


class TLog():
    def __init__(self, aFile):
        self.File = aFile

    def Print(self, aMsg: str):
        print('%s, %s' % (datetime.now().strftime('%d/%m/%Y %H:%M:%S') ,aMsg))

        with open(self.File, 'a+') as FileH:
            FileH.write(aMsg + '\n')


class THeader():
    def __init__(self):
        self.OS = ['Macintosh; Intel Mac OS X 10_15_5', 'Windows NT 10.0; Win64; x64; rv:77', 'Linux; Intel Ubuntu 20.04']
        self.Browser = ['Chrome/83', 'Firefox/77', 'Opera/45']

    def Get(self):
        OS = self.OS[randint(0, len(self.OS) - 1)]
        Browser = self.Browser[randint(0, len(self.Browser)) - 1]
        return {
            'Accept': '*/*',
            'User-Agent': 'Mozilla/5.0 (%s) %s' % (OS, Browser)
        }


class THttpScraper():
    def __init__(self, aRoot: str, aMaxTask = 16, aSleep: float = 0.1):
        self.Root = aRoot
        self.MaxTask = aMaxTask
        self.Sleep = aSleep

        self.Url = []
        self.UrlCnt = 0
        self.TotalData = 0

        self.Queue = asyncio.Queue()
        self.Queue.put_nowait(aRoot)

        FileLog = '%s_%s.log' % (self.__class__.__name__, urlparse(aRoot).hostname)
        self.Log = TLog(FileLog)

    async def _GrabHref(self, aUrl: str, aData: str):
        Msg = 'URL found:%d, URL done:%d, Total:%dM, URL:%s' % (len(self.Url), self.UrlCnt, self.TotalData / 1000000, aUrl)
        self.Log.Print(Msg.strip())

        self.TotalData += len(aData)
        self.UrlCnt += 1

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
                   (not Href in self.Url) and \
                   (not Ext in ['.zip', '.jpg', '.png']):
                    self.Url.append(Href)
                    self.Queue.put_nowait(Href)

    async def _Fetch(self, aSession):
        while True:
            Url = await self.Queue.get()
            await asyncio.sleep(self.Sleep)

            try:
                async with aSession.get(Url) as Response:
                    Data = await Response.read()
                    if (Data):
                        await self._GrabHref(Url, Data)

            except (aiohttp.ClientConnectorError, aiohttp.ClientError) as E:
                self.Log.Print('_Fetch_A %s %s' % (E, Url))
            except Exception as E:
                self.Log.Print('_Fetch_B %s %s' % (E, Url))

            self.Queue.task_done()

    async def Parse(self):
        Header = THeader()
        async with aiohttp.ClientSession(headers=Header.Get()) as Session:
            Tasks = []
            for i in range(self.MaxTask):
                Task = asyncio.create_task(self._Fetch(Session))
                Tasks.append(Task)

            self.Log.Print('URL:%s, Tasks:%d' % (self.Root, len(asyncio.all_tasks())))
            await self.Queue.join()
            self.Log.Print('Done')


class TMain():
    async def _Scheduler(self, aUrl: str, aSemaph):
        async with aSemaph:
            Scraper = THttpScraper(aUrl, 64, 1)
            await Scraper.Parse()

    async def CreateTasks(self, aUrl: list, aMaxTasks: int):
        Semaph = asyncio.Semaphore(aMaxTasks)

        Tasks = []
        for Url in aUrl:
            if (not Url.startswith('-')):
                Task = asyncio.create_task(self._Scheduler(Url, Semaph))
                Tasks.append(Task)
        await asyncio.gather(*Tasks)

    def Run(self, aUrl: list, aMaxTasks: int = -1):
        if (aMaxTasks == -1):
            aMaxTasks = len(aUrl)

        Task = self.CreateTasks(aUrl, aMaxTasks)
        asyncio.run(Task)


def Test1():
    Hosts = ['https://kaluna.te.ua']
    #Hosts = ['http://oster.com.ua']
    #Hosts = ['http://bereka-radio.com.ua']
    #Hosts = ['https://largo.com.ua']
    #Hosts = ['https://www.neotec.ua', 'https://largo.com.ua', 'http://oster.com.ua', 'http://bereka-radio.com.ua', 'https://kaluna.te.ua']
    StartT = time.time()
    Main = TMain()
    Main.Run(Hosts)
    print('duration (s)', round(time.time() - StartT, 2))

Test1()
