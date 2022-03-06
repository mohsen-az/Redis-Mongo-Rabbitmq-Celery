"""
    Distributing tasks among workers(consumer)
    Message durability
    Manual acknowledge
    Quality Of Service
"""

import pika
import random

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost')
)

channel = connection.channel()

channel.queue_declare(
    queue='logs',
    durable=True
)

channel.basic_publish(
    exchange='',
    routing_key='logs',
    body=bytes(f'Message {random.randint(1, 100)}', 'utf-8'),
    properties=pika.BasicProperties(
        delivery_mode=2
    )
)

print('Message send to queue')

connection.close()
