import pika

from basic.utils import greeting_callback

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost')
)

channel = connection.channel()

channel.queue_declare(
    queue='logs',
    durable=True
)

channel.basic_qos(prefetch_count=1)

channel.basic_consume(
    queue='logs',
    on_message_callback=greeting_callback,
)

channel.start_consuming()
