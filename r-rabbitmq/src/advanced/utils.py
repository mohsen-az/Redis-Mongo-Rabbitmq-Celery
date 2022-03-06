def greeting_callback(channel, method, properties, body):
    print(f'Message received: {body}')

    # Custom auto_ack parameters
    # Send ack to server rabbitmq after run successfully callback method
    channel.basic_ack(delivery_tag=method.delivery_tag)
