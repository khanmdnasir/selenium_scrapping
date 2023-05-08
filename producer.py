import pika

def publish():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.basic_publish(exchange='', routing_key='update_queue', body='Update Producs')
    channel.close()

publish()