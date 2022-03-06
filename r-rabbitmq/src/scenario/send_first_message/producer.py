import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost')
)

channel = connection.channel()

channel.queue_declare(
    queue='echo'
)

channel.basic_publish(
    exchange='',  # direct default
    routing_key='echo',
    body=b'Hello World!'
)

print('Message send to queue')

connection.close()
