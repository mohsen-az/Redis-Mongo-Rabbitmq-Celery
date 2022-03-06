import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost')
)

channel = connection.channel()

channel.exchange_declare(
    exchange='direct_logs',
    exchange_type='direct'
)

messages = {
    'info': 'INFO Message',
    'error': 'ERROR Message',
    'warning': 'WARNING Message'
}

for type_message, text_message in messages.items():
    channel.basic_publish(
        exchange='direct_logs',
        routing_key=type_message,
        body=bytes(text_message, 'utf-8')
    )

connection.close()
