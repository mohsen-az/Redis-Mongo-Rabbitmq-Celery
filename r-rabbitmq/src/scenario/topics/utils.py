import random
import time


def greeting_callback(ch, method, properties, body):
    print(f'Message received: {body}')
    time.sleep(random.randint(1, 5))


def error_greeting_callback(ch, method, properties, body):
    print(f'Message received: {body}')

    with open(f'log/error_logs.log', mode='a') as file_handler:
        file_handler.write(f'[*] {body}\n')
    time.sleep(random.randint(1, 5))
