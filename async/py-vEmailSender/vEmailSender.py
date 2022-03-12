'''
Python async
Send eMail example
VladVons@gmail.com
2022.03.11
'''

__version__ = '1.0.1'


import asyncio
import aiosmtplib
import random
import json
from email.message import EmailMessage
from datetime import datetime

        
class TLog():
    def __init__(self, aFile):
        self.File = aFile
        
    def Print(self, aMsg: str):
        Msg = '%s, %s' % (datetime.now().strftime('%H:%M:%S'), aMsg)
        print(Msg)
        
        with open(self.File, 'a+') as FileH:
            FileH.write(Msg + '\n')
    

class TMail():
    def __init__(self, aFile: str):
        self.CntDone = 0

        with open(aFile, 'r') as hFile: 
            self.Conf = json.load(hFile)
        self.ConfOption = self.Conf.get('Option', {})

        self.Queue = asyncio.Queue()
        for Item in self.Conf.get('MailTo', []):
            self.Queue.put_nowait(Item)

        self.Log = TLog(aFile + '.log')

    async def Send(self, aMailTo: str, aTaskId: int):
        Smtp = random.choice(self.Conf['Smtp']).copy()
        MailData = random.choice(self.Conf['MailData'])

        EMsg = EmailMessage()
        EMsg["From"] = Smtp.get('from')
        EMsg["To"] = aMailTo
        EMsg["Subject"] = MailData.get('subj') + ' ' + str(self.CntDone)
        EMsg.set_content(MailData.get('body'))

        self.Log.Print('MailTo:%s, Done:%d' % (aMailTo, self.CntDone))
        Smtp.pop('from', None)
        await aiosmtplib.send(EMsg, **Smtp)

    async def _Worker(self, aTaskId: int):
        Loop = 0
        self.IsRun = True
        ConfSleep = self.Conf.get('Sleep', 3)

        await asyncio.sleep(aTaskId)
        while (self.IsRun) and (not self.Queue.empty()):
            Loop += 1

            try:
                EMail = await asyncio.wait_for(self.Queue.get(), timeout = 0.5)
                await self.Send(EMail, aTaskId)
                self.CntDone += 1
            except aiosmtplib.errors.SMTPDataError as E:
                self.Log.Print('Err smtp:%s' % (E))
                await asyncio.sleep(ConfSleep * 10)
            except Exception as E:
                self.Log.Print('Err:%s' % (E))
            finally:
                self.Queue.task_done()

            await asyncio.sleep(ConfSleep)

    async def Run(self):
            self.Log.Print('Start')
            Tasks = [asyncio.create_task(self._Worker(i)) for i in range(self.ConfOption.get('MaxTasks', 5))]
            await asyncio.gather(*Tasks)
            self.IsRun = False


if (__name__ == '__main__'):
    print(__version__)
    File = 'vEmail_A.json'
    asyncio.run(TMail(File).Run())
