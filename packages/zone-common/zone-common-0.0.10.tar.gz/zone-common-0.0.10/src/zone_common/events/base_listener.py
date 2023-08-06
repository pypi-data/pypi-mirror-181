from abc import ABC, abstractmethod, abstractproperty
from nats.js.api import AckPolicy, DeliverPolicy, ConsumerConfig
from nats.aio.client import Client as NATS
import json
import asyncio as aio


class Listener:

    @abstractproperty
    def subject(self):
        pass

    @abstractproperty
    def queueGroupName(self):
        pass

    @abstractmethod
    def onMessage(self, data, message) -> None:
        pass

    ack_wait = 5

    def __init__(self, client: NATS):
        self.client = client

    async def listen(self):
        js = self.client.jetstream()

        async def subscribe_handler(msg):
            subject = msg.subject
            print("Received a message on '{subject}'".format(
                subject=subject))

            parsedData = self.parseMessage(msg)
            aio.create_task(self.onMessage(parsedData, msg))

        config = ConsumerConfig(
            deliver_subject=self.queueGroupName,
            deliver_group=self.queueGroupName,
            ack_wait=self.ack_wait,
            ack_policy=AckPolicy.EXPLICIT,
            deliver_policy=DeliverPolicy.ALL,
            durable_name=self.queueGroupName
        )

        await js.subscribe(self.subject, queue=self.queueGroupName, manual_ack=True, config=config, cb=subscribe_handler)

    def parseMessage(self, msg):
        data = msg.data.decode()
        return json.loads(data)
