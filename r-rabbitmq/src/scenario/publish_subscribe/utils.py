import random
import time


def greeting_callback(ch, method, properties, body):
    print(f'Message receive: {body}')
    time.sleep(random.randint(1, 10))
    print('Task Done!!!')
    ch.basic_ack(delivery_tag=method.delivery_tag)
