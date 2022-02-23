#!/usr/bin/python3 -B

import asyncio
import aiohttp

async def Test1():
  from aiohttp_socks.connector import ProxyConnector, ProxyClientRequest

  async with aiohttp.ClientSession() as session:
    async with session.get('http://icanhazip.com/') as resp:
      body = await resp.text()
      host_ip = body.strip()
      print('ip: {}'.format(host_ip))

  conn = ProxyConnector(remote_resolve=False)
  try:
    async with aiohttp.ClientSession(connector=conn, request_class=ProxyClientRequest) as session:
      async with session.get('http://icanhazip.com/', proxy='socks5://127.0.0.1:9060') as resp:
        body = await resp.text()
        tor_ip = body.strip()
        print('tor ip: {}'.format(tor_ip))
  except aiohttp.ClientProxyConnectionError:
    # connection problem
    pass

  except aiohttp.ClientConnectorError:
    # ssl error, certificate error, etc
    pass
  except aiosocks.SocksError:
    # communication problem
    pass

def Test2():
    import requests

    session = requests.session()
    session.proxies['http'] = 'socks5h://localhost:9050'
    session.proxies['https'] = 'socks5h://localhost:9050'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:60.0) Gecko/20100101 Firefox/60.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    }

    url = 'https://brain.com.ua'
    res = session.get(url, headers=headers)
    print(res)



def Test3():
    import asyncio
    import aiohttp
    from aiohttp_socks import SocksConnector

    async def fetch(session, aId):
        url = 'http://icanhazip.com'
        async with session.get(url) as res:
            #return res.text
            return await res.read()

    async def main(id):
        #Proxy = 'socks4://localhost:9050'
        #Proxy = 'socks5://localhost:9050'
        Proxy = 'socks5t://localhost:9050'
        connector = SocksConnector.from_url(Proxy)
        async with aiohttp.ClientSession(connector=connector) as session:
            res = await fetch(session, id)
            print(res)

    loop = asyncio.get_event_loop()
    future = [asyncio.ensure_future(main(id)) for id in range(3)]
    loop.run_until_complete(asyncio.wait(future))


class TTorProxy():
    Url = 'http://icanhazip.com'

    async def _Worker(self, aSession, aTaskId: int):
        async with aSession.get(self.Url) as Response:
            Data = await Response.read()
            print(aTaskId, Response.status,  Data)

    async def Run(self):
        Headers = {
            'Accept': '*/*',
            'User-Agent': 'Mozilla/5.5 (Windows NT 6.1; rv:60.0) Gecko/20100101 Firefox/60.0'
        }

        Proxy = 'socks5t://localhost:9050'
        Connector = SocksConnector.from_url(Proxy)

        async with aiohttp.ClientSession(headers=Headers, connector=Connector) as Session:
            Tasks = [self._Worker(Session, i) for i in range(10):
            await asyncio.gather(*Tasks)


asyncio.run(TTorProxy.Run())



