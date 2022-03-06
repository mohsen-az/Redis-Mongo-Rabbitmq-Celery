"""
    Manual Exchange
    Bind Queue And Exchange
"""
import random

import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost')
)

channel = connection.channel()

channel.exchange_declare(
    exchange='logs',
    exchange_type='fanout'
)

channel.basic_publish(
    exchange='logs',
    routing_key='',
    body=bytes(f'Message {random.randint(1, 100)}', 'utf-8')
)

print('Message send to queues')

connection.close()
