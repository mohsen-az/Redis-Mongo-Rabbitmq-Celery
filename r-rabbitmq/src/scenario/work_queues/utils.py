import random
import time


def greeting_callback(ch, method, properties, body):
    print(f'Message received: {body}')
    time.sleep(random.randint(5, 10))
    print('Task Done')
    ch.basic_ack(delivery_tag=method.delivery_tag)  # manual acknowledge
