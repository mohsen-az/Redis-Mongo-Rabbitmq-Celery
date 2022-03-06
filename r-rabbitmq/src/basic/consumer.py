from rabbit_connection import RabbitMQ
from crawler.utils import greeting_callback

rabbit = RabbitMQ()

channel = rabbit.connection.channel()

# Declare Queue(Fix)
channel.queue_declare(queue="echo", durable=False)  # durable ==> persistence(redis)[Save messages in disk]

# Consume message and send to callback function
channel.basic_consume(
    queue="echo",
    on_message_callback=greeting_callback,
    # Send ack to server rabbitmq after receive message[Default ack]
    # auto_ack=True  # acknowledgement
)

print("Waiting Message...")

# Run blocking connection(while true)
channel.start_consuming()
