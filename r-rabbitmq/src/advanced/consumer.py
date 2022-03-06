from rabbit_connection import RabbitMQ
from crawler.utils import greeting_callback

rabbit = RabbitMQ()

channel = rabbit.connection.channel()

# Declare Exchange
channel.exchange_declare(
    exchange="logs",
    exchange_type="fanout"
)

# Create empty queue with random name
queue = channel.queue_declare("")
# Save queue name
queue_name = queue.method.queue

# Bind queue and exchange
channel.queue_bind(
    queue=queue_name,
    exchange="logs",
    routing_key="echo"
)

# Consume message and send to callback function
channel.basic_consume(
    queue=queue_name,
    on_message_callback=greeting_callback,
    # auto_ack=True  # acknowledgement
)

print("Waiting Message...")

# Run blocking connection(while true)
channel.start_consuming()
