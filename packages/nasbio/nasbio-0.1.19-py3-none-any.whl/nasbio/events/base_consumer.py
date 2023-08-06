from typing import Any
from abc import ABC, abstractmethod

import json
from pika import BlockingConnection

from .types import Subjects


class AbstractConsumer(ABC):
    @property
    @abstractmethod
    def subject(self) -> Subjects | str:
        raise NotImplementedError()

    def callback(self, ch, method, properties, body: bytes):
        self.on_message(json.loads(body.decode('utf-8')))

    @abstractmethod
    def on_message(self, data: Any):
        raise NotImplementedError()

    def __init__(self, connection: BlockingConnection):
        self.channel = connection.channel()  # Start a channel.
        self.channel.queue_declare(queue=self.subject)  # Declare a queue.
        self.channel.basic_consume(queue=self.subject, on_message_callback=self.callback, auto_ack=True)

    def run(self):
        print(f"Start consuming on queue '{self.subject}'...")
        self.channel.start_consuming()
