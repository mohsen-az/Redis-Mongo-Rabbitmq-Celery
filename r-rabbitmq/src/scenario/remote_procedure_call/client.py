import random

import pika
import uuid


class Client:

    def __init__(self):
        self.response = None
        self.correlation_id = None

        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost')
        )
        self.channel = self.connection.channel()

        q = self.channel.queue_declare(
            queue='',
            exclusive=True
        )
        self.q_name = q.method.queue

        self.client_consumer()

    def client_callback(self, ch, method, properties, body):
        if self.correlation_id == properties.correlation_id:
            self.response = body

    def client_consumer(self):
        self.channel.basic_consume(
            queue=self.q_name,
            on_message_callback=self.client_callback,
            auto_ack=True
        )

    def client_producer(self, number):
        self.correlation_id = str(uuid.uuid4())

        self.channel.basic_publish(
            exchange='',
            routing_key='rpc_queue',
            body=bytes(str(number), 'utf-8'),
            properties=pika.BasicProperties(
                reply_to=self.q_name,
                correlation_id=self.correlation_id
            )
        )

        while self.response is None:
            self.connection.process_data_events()
        return int(self.response)


if __name__ == '__main__':
    client = Client()
    result = client.client_producer(number=random.randint(1, 100))
    print(result)
