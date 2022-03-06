from rabbit_connection import RabbitMQ

from utils import greeting_callback

rabbit = RabbitMQ()

channel = rabbit.connection.channel()

channel.exchange_declare(
    exchange="crawler",
    exchange_type="direct"
)

queue = channel.queue_declare(queue="")
queue_name = queue.method.queue

channel.queue_bind(
    queue=queue_name,
    exchange="crawler",
    routing_key="links"
)

channel.basic_qos(prefetch_count=1)

channel.basic_consume(
    queue=queue_name,
    on_message_callback=greeting_callback,
    auto_ack=False
)

print("Waiting Link...")
channel.start_consuming()