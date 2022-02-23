#!/usr/bin/python3 -B

'''
apt-get install tor python3-stem privoxy
pip3 install asyncio aiohttp aiohttp-socks
'''

import asyncio
import aiohttp
from aiohttp_socks import SocksConnector


class TTorProxy():
    Url = 'http://icanhazip.com'

    Proxy = 'socks5://localhost:9050'

    Headers = {
        'Accept': '*/*',
        'User-Agent': 'Mozilla/5.5 (Windows NT 6.1; rv:60.0) Gecko/20100101 Firefox/60.0'
    }

    async def _Worker(self, aSession, aTaskId: int):
        async with aSession.get(self.Url) as Response:
            Data = await Response.read()
            print('TaskId: %d, Status: %d, Data: %s' % (aTaskId, Response.status, Data.decode().strip()))

    async def Run(self, aProxy: bool, aTaskCnt: int):
        if (aProxy):
            Connector = SocksConnector.from_url(self.Proxy)
        else:
            Connector = None

        async with aiohttp.ClientSession(headers=self.Headers, connector=Connector) as Session:
            Tasks = [asyncio.create_task(self._Worker(Session, i)) for i in range(aTaskCnt)]
            await asyncio.gather(*Tasks)


asyncio.run(TTorProxy().Run(False, 10))
asyncio.run(TTorProxy().Run(True, 10))
