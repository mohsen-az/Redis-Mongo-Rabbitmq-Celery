from rabbit_connection import RabbitMQ

rabbit = RabbitMQ()

channel = rabbit.connection.channel()

# Declare Exchange
channel.exchange_declare(
    exchange="logs",
    exchange_type="fanout"  # Send message to every queue bind to exchange
)

"""
exchange_type="fanout" | Send message to every queue that bind to exchange
exchange_type="direct" | Send message to queue that bind to exchange with routing key
exchange_type="topic" | Send message to queue that bind to exchange with routing key(pattern)
exchange_type="headers"
"""


# Publish message to exchange -> queue
channel.basic_publish(
    exchange="logs",  # Custom Exchange
    routing_key="echo",  # Search queue
    body=b"Hello Rabbit"
)

# Close Connection
channel.close()
