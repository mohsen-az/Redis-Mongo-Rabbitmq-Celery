import pika

from basic.utils import greeting_callback

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost')
)

channel = connection.channel()

channel.exchange_declare(
    exchange='logs',
    exchange_type='fanout'
)

q = channel.queue_declare(
    queue='',
    exclusive=True
)

q_name = q.method.queue

# Binding queue and exchange
channel.queue_bind(
    queue=q_name,
    exchange='logs'
)

channel.basic_consume(
    queue=q_name,
    on_message_callback=greeting_callback
)

print('Waiting for message')
print(f'Queue name: {q_name}')

channel.start_consuming()
