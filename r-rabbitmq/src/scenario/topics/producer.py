import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost')
)

channel = connection.channel()

channel.exchange_declare(
    exchange='topic_logs',
    exchange_type='topic'
)

messages = {
    'error.warning.important': 'Important Message',
    'info.debug.nonimportant': 'NonImportant Message'
}

for type_message, text_message in messages.items():
    channel.basic_publish(
        exchange='topic_logs',
        routing_key=type_message,
        body=bytes(text_message, 'utf-8')
    )

connection.close()
