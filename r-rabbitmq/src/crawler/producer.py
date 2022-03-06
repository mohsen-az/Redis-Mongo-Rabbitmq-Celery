from rabbit_connection import RabbitMQ

from crawl import crawl_links

rabbit = RabbitMQ()

channel = rabbit.connection.channel()

channel.exchange_declare(
    exchange="crawler",
    exchange_type="direct"
)

for link in crawl_links():
    channel.basic_publish(
        exchange="crawler",
        routing_key="links",
        body=f"{link}"
    )
channel.close()
