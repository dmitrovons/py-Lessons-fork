#!/usr/bin/env python3

'''
python async example
VladVons@gmail.com
2021.04.09
https://steemit.com/python/@gunhanoral/python-asyncio-port-scanner
'''


import asyncio
import time
import random


class TPortScan():
    MaxConn = 1015
    TimeOut = 3
    _CntAll = 0
    _CntOpen = 0

    def GetIpRange_1(self, aCidr: str) -> list:
        import ipaddress
        Res = [str(IP) for IP in ipaddress.IPv4Network(aCidr)]
        return Res

    def GetIpRange(self, aCidr: str) -> list:
        import socket
        import struct

        Ip, Cidr = aCidr.split('/')
        Cidr = int(Cidr)
        Bits = 32 - Cidr
        if (Bits == 0):
            return [Ip]

        i = struct.unpack('>I', socket.inet_aton(Ip))[0]
        Start = (i >> Bits) << Bits
        End = Start | ((1 << Bits) - 1)
        Res = []
        for i in range(Start, End):
            Addr = socket.inet_ntoa(struct.pack('>I', i))
            Res.append(Addr)
        #Uniq = set(Res)
        return Res

    def FilterOpened(self, aList: list, aValue: bool) -> list:
        return [Item for Item in aList if Item[2] == aValue]

    async def CheckPort(self, aIp: str, aPort: int) -> bool:
        #print('CheckPort', aIp, aPort)
        Conn = asyncio.open_connection(aIp, aPort)
        try:
            Reader, Writer = await asyncio.wait_for(Conn, timeout=self.TimeOut)
            self._CntOpen += 1
            return True
        except:
            return False
        finally:
            self._CntAll += 1
            if (self._CntAll > 0) and (self._CntAll % 1000 == 0):
                print('CntAll', self._CntAll, 'CntOpen', self._CntOpen)

            if ('Writer' in locals()):
                Writer.close()

    async def CheckPortSem(self, aSem, aIp: str, aPort: int) -> tuple:
        #print('CheckPortSem', aIp, aPort)
        async with aSem:
            Opened = await self.CheckPort(aIp, aPort)
            return (aIp, aPort, Opened)

    async def Main(self, aHosts: list, aPorts: list):
        print('Main. create tasks')
        Sem = asyncio.Semaphore(self.MaxConn)
        Tasks = []
        for Host in aHosts:
            for Port in aPorts:
                Task = asyncio.create_task(self.CheckPortSem(Sem, Host, Port))
                Tasks.append(Task)

        print('Main. launch tasks', len(Tasks))
        Res = await asyncio.gather(*Tasks)
        return Res


def SpeedTest():
    from Conf import Hosts, Ports

    PortScan = TPortScan()
    StartT = time.time()
    Task = PortScan.Main(Hosts, Ports)
    Res = asyncio.run(Task)
    Res = PortScan.FilterOpened(Res, True)
    for Item in Res:
        print(Item)
    print('Opened', len(Res))

    print('async duration (s)', round(time.time() - StartT, 2))

def Scan():
    Ports = [80]
    #Hosts = ['192.168.11.131', '192.168.11.132', '192.168.11.133', '192.168.11.134', '192.168.11.135', '192.168.11.136']
    Hosts = ['192.168.2.131', '192.168.2.132']

    while True:
        PortScan = TPortScan()
        Task = PortScan.Main(Hosts, Ports)
        Res = asyncio.run(Task)
        Res = PortScan.FilterOpened(Res, True)
        for Item in Res:
            print(Item)
        print('done')
        time.sleep(3)

#SpeedTest()
Scan()
