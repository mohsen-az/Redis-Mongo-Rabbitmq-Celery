def greeting_callback(ch, method, properties, body):
    print(f'Message received: {body}')
