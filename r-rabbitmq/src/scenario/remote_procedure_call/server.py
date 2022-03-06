import time

import pika


class Server:

    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost')
        )
        self.channel = self.connection.channel()

        self.channel.queue_declare(
            queue='rpc_queue'
        )

        self.server_consumer()

    def server_callback(self, ch, method, properties, body):
        print('Start Processing')
        time.sleep(5)

        processing = self.process(body)
        self.server_producer(ch, method, properties, body=processing)
        ch.basic_ack(delivery_tag=method.delivery_tag)

        print('End Processing')

    def server_consumer(self):
        print('Waiting Message')

        self.channel.basic_qos(prefetch_count=1)

        self.channel.basic_consume(
            queue='rpc_queue',
            on_message_callback=self.server_callback
        )
        self.channel.start_consuming()

    @staticmethod
    def server_producer(ch, method, properties, body):
        ch.basic_publish(
            exchange='',
            routing_key=properties.reply_to,
            body=bytes(str(body), 'utf-8'),
            properties=pika.BasicProperties(
                correlation_id=properties.correlation_id
            )
        )

    @staticmethod
    def process(body):
        return int(body) + 1


if __name__ == '__main__':
    server = Server()
