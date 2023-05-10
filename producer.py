import pika

def publish():
    connection = pika.BlockingConnection(pika.URLParameters('amqps://nnfglkbu:mTd4zSMjdSg3YPUDkK9gO2TQXY1DONVM@armadillo.rmq.cloudamqp.com/nnfglkbu'))
    channel = connection.channel()
    channel.basic_publish(exchange='', routing_key='update_queue', body='Update Products')
    channel.close()

if __name__ == '__main__':
    publish()