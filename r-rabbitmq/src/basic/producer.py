from rabbit_connection import RabbitMQ

rabbit = RabbitMQ()

channel = rabbit.connection.channel()

# Declare Queue
channel.queue_declare(queue="echo", durable=False)

# Publish message to exchange -> queue
channel.basic_publish(
    exchange="",  # Default Exchange
    routing_key="echo",  # Search queue
    body=b"Hello Rabbit"
)

# Close Connection
channel.close()
