#!/usr/bin/python3 -B

'''
python async tor proxy
VladVons@gmail.com
2022.02.23

apt-get install tor python3-stem privoxy
pip3 install asyncio aiohttp aiohttp-socks

https://gist.github.com/DusanMadar/8d11026b7ce0bce6a67f7dd87b999f6b
'''

import time
import asyncio
import aiohttp
from aiohttp_socks import ProxyConnector


class TTorProxy():
    def __init__(self):
        #self.Url = 'http://icanhazip.com'
        self.Url = 'https://ipinfo.io/json'
        #self.Url = 'https://brain.com.ua/ukr'

        self.Proxy = 'socks5://localhost:9050'
        self.Headers = {
            'Accept': '*/*',
            'User-Agent': 'Mozilla/5.5 (Windows NT 6.1; rv:60.0) Gecko/20100101 Firefox/60.0'
        }

    def GetConnector(self, aProxy: bool):
        if (aProxy):
            return ProxyConnector.from_url(self.Proxy)

    async def _Worker(self, aSession, aTaskId: int):
        #await asyncio.sleep(5)
        try:
            async with aSession.get(self.Url) as Response:
                Data = await Response.read()
                print('TaskId: %d, Status: %d, Data: %s' % (aTaskId, Response.status, Data.decode().strip()))
                #print('---x1', Response.cookies, type(Response.cookies))

        except (aiohttp.ClientConnectorError, aiohttp.ClientError) as E:
            print('Exception', E, self.Url)

    async def Run(self, aProxy: bool = True, aTaskCnt: int = 10):
        #cookie_jar = aiohttp.CookieJar(unsafe=True)
        #cookie_jar = aiohttp.DummyCookieJar()

        async with aiohttp.ClientSession(headers=self.Headers, connector=self.GetConnector(aProxy)) as Session:
            Tasks = [asyncio.create_task(self._Worker(Session, i)) for i in range(aTaskCnt)]
            await asyncio.gather(*Tasks)

def Main():
    Duration = []
    for IsProxy in [True]:
        TimeStart = time.time()
        asyncio.run(TTorProxy().Run(IsProxy, 1))
        TimeDur = time.time() - TimeStart
        Duration.append(TimeDur)

        print('Proxy %s, Time: %.3f' % (IsProxy, TimeDur))
        print()
    print('Duration', Duration)

Main()