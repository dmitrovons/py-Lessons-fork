#!/usr/bin/env python3

'''
python async example
VladVons@gmail.com
2022.03.28
'''

import time
import asyncio
import aiohttp
from urllib.parse import urlparse


class TDownload():
    def WriteFile(self, aName: str, aData):
        print('WriteFile', aName)
        with open(aName, 'wb') as FileH:
            FileH.write(aData)

    async def Fetch(self, aUrl: str, aSession, aIdx: int) -> tuple:
        try:
            async with aSession.get(aUrl) as Response:
                print('Fetch', aIdx, aUrl)
                Data = await Response.read()
                if (Response.status == 200):
                    Path = urlparse(aUrl)
                    File = ('f_%s%s' % (Path.netloc, Path.path)).replace('/', '_')
                    self.WriteFile(File, Data)
                else:
                    print('Err', Response.status, aUrl)
                return (Response.status, aUrl)
        except Exception as E:
            print('Err:', E)

    async def Get(self, aUrl: list):
        async with aiohttp.ClientSession() as Session:
            print('Main. create tasks', len(aUrl))
            Tasks = [asyncio.create_task(self.Fetch(Val, Session, Idx)) for Idx, Val in enumerate(aUrl)]

            print('Main. launch tasks')
            return await asyncio.gather(*Tasks)

    async def LoadFromFile(self, aFile: str):
        with open(aFile, 'r') as F:
            List = F.read().splitlines()
            List = ['%s/sitemap.xml' % i for i in List]
            Res = await self.Get(List)
            for i in Res:
                print(i)


StartT = time.time()
Task = TDownload().LoadFromFile('hotline_min.txt')
asyncio.run(Task)
print('async duration (s)', round(time.time() - StartT, 2))
