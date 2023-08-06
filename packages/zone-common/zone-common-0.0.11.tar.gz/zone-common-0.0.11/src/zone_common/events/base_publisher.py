from abc import ABC, abstractproperty
import asyncio as aio
from nats.aio.client import Client as NATS
import json


class Publisher(ABC):

    @abstractproperty
    def subject(self):
        pass

    def __init__(self, client):
        self.client = client

    async def publish(self, data):
        parsedData = bytes(json.dumps(data), 'utf-8')
        await self.client.publish(self.subject, parsedData)
        print(f'Published [{self.subject}] : {json.dumps(data)}')
