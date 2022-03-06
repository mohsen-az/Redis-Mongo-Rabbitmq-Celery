import pika

from basic.utils import greeting_callback

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost')
)

channel = connection.channel()

channel.exchange_declare(
    exchange='topic_logs',
    exchange_type='topic'
)

q = channel.queue_declare(
    queue='',
    exclusive=True
)

q_name = q.method.queue

binding_key = '#.nonimportant'

channel.queue_bind(
    queue=q_name,
    exchange='topic_logs',
    routing_key=binding_key
)

print('Waiting for message')

channel.basic_consume(
    queue=q_name,
    on_message_callback=greeting_callback,
    auto_ack=True
)

channel.start_consuming()
