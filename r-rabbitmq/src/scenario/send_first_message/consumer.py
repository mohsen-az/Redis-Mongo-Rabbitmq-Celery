import pika

from basic.utils import greeting_callback

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost')
)

channel = connection.channel()

channel.queue_declare(
    queue='echo'
)

channel.basic_consume(
    queue='echo',
    on_message_callback=greeting_callback,
    auto_ack=True
)

print('Waiting for message')

channel.start_consuming()
