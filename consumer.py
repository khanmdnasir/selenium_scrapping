import pika
from baseBot import BaseBot
connection = pika.BlockingConnection(pika.URLParameters('amqps://nnfglkbu:mTd4zSMjdSg3YPUDkK9gO2TQXY1DONVM@armadillo.rmq.cloudamqp.com/nnfglkbu'))
channel = connection.channel()

channel.queue_declare(queue='update_queue')

def callback(ch, method, properties, body):
    print(body)
    try:
        bot = BaseBot()
        bot.update()
    except Exception as e:
        print(str(e))

channel.basic_consume(queue='update_queue', on_message_callback=callback, auto_ack=True)

channel.start_consuming()
